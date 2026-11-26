"""Marriage system"""

import logging
import random
import sqlite3
import time
from pathlib import Path

import discord
from discord.ext import commands, tasks

from commands.jobs import DB_PATH
from commands.shop import create_inventory_database

GIF_PATH = (
    Path(__file__).resolve().parent.parent
    / 'assets' / 'gifs' / 'divider1.gif'
)

FOOTER = "THE REAL OLROX • Richter's childhood nightmare."
LEVELS = (
    (0, 'Newlyweds', '💍'),
    (7, 'In Love', '🌹'),
    (30, 'Soulmates', '💜'),
)
LOG = logging.getLogger(__name__)

GIF_DIR = Path(__file__).resolve().parent.parent / "assets" / "gifs"

LOVE_GIFS = [
    *GIF_DIR.glob("love*.gif"),
]


def create_marriage_database():
    create_inventory_database()
    with sqlite3.connect(DB_PATH, timeout=10) as db:
        db.execute('''CREATE TABLE IF NOT EXISTS marriages (
            guild_id INTEGER NOT NULL, user_one INTEGER NOT NULL,
            user_two INTEGER NOT NULL, married_at INTEGER NOT NULL,
            PRIMARY KEY (guild_id, user_one, user_two))''')


def get_marriage(guild_id, user_id, db=None):
    if db is None:
        with sqlite3.connect(DB_PATH, timeout=10) as connection:
            return get_marriage(guild_id, user_id, connection)
    return db.execute('''SELECT user_one, user_two, married_at FROM marriages
        WHERE guild_id = ? AND (user_one = ? OR user_two = ?)''',
        (guild_id, user_id, user_id)).fetchone()


def has_ring(guild_id, user_id):
    with sqlite3.connect(DB_PATH, timeout=10) as db:
        return db.execute('''SELECT 1 FROM inventory WHERE guild_id = ?
            AND user_id = ? AND item_id = 'engagement_ring'
            AND quantity > 0''',
            (guild_id, user_id)).fetchone() is not None


def create_marriage(guild_id, first, second, consume_ring=True):
    if first == second:
        return 'self'
    with sqlite3.connect(DB_PATH, timeout=10) as db:
        db.execute('BEGIN IMMEDIATE')
        if (
            get_marriage(guild_id, first, db)
            or get_marriage(guild_id, second, db)
        ):
            return 'married'
        if consume_ring:
            result = db.execute('''UPDATE inventory SET quantity = quantity - 1
                WHERE guild_id = ? AND user_id = ?
                AND item_id = 'engagement_ring' AND quantity > 0''',
                (guild_id, first))
            if result.rowcount != 1:
                return 'ring'
        a, b = sorted((first, second))
        db.execute('INSERT INTO marriages VALUES (?, ?, ?, ?)',
                   (guild_id, a, b, time.time_ns()))
    return 'success'


def delete_marriage(guild_id, record):
    with sqlite3.connect(DB_PATH, timeout=10) as db:
        result = db.execute('''DELETE FROM marriages WHERE guild_id = ?
            AND user_one = ? AND user_two = ? AND married_at = ?''',
            (guild_id, *record))
        return result.rowcount == 1


def marriage_level(record):
    days = max(0, int((time.time() - record[2] / 1e9) // 86400))
    level = max(
        (entry for entry in LEVELS if days >= entry[0]),
        key=lambda e: e[0],
    )
    return days, level


class DecisionView(discord.ui.View):
    """Restrict decisions to the intended member."""

    def __init__(self, cog, owner_id):
        super().__init__(timeout=120)
        self.cog = cog
        self.owner_id = owner_id
        self.message = None
        self.finished = False

    async def interaction_check(self, interaction):
        if interaction.user.id != self.owner_id or self.finished:
            await interaction.response.send_message(
                'This decision is not yours.',
                ephemeral=True,
            )
            return False
        return True

    def close(self):
        self.finished = True
        for item in self.children:
            item.disabled = True
        self.stop()

    async def on_timeout(self):
        self.close()
        if self.message:
            try:
                await self.message.edit(view=self)
            except discord.HTTPException:
                pass

    async def finish(self, interaction, title, description):
        self.close()
        embed = self.cog.embed(title, description)

        if interaction.message and interaction.message.embeds:
            thumbnail = interaction.message.embeds[0].thumbnail.url

            if thumbnail:
                embed.set_thumbnail(url=thumbnail)

        await interaction.response.edit_message(
            embed=embed,
            view=self,
        )


class ProposalView(DecisionView):
    def __init__(self, cog, proposer, target):
        super().__init__(cog, target.id)
        self.proposer = proposer
        self.target = target

    @discord.ui.button(
        label='Accept',
        emoji='💍',
        style=discord.ButtonStyle.success,
    )
    async def accept(self, interaction, button):
        if self.finished:
            return await interaction.response.send_message(
                'This proposal is closed.',
                ephemeral=True,
            )
        guild = interaction.guild
        if guild.get_member(self.proposer.id) is None:
            return await self.finish(
                interaction,
                'A LOST PROMISE',
                'The proposer is no longer here.',
            )
        status = create_marriage(guild.id, self.proposer.id, self.target.id)
        if status != 'success':
            reason = (
                'The ring is no longer available.' if status == 'ring'
                else 'One of you is already married, oh the drama'
            )
            return await self.finish(interaction, 'A LOST PROMISE', reason)
        await self.finish(
            interaction,
            'ETERNAL BOND',
            f'{self.proposer.mention} and {self.target.mention} '
            'are now married.\n\n'
            '*May your devotion outlive the night!*',
        )
        await self.cog.sync_roles(guild, (self.proposer.id, self.target.id))

    @discord.ui.button(
        label='Decline',
        emoji='🥀',
        style=discord.ButtonStyle.danger,
    )
    async def decline(self, interaction, button):
        await self.finish(
            interaction,
            'DECLINED PROMISE',
            'Not everyone is meant to be together.\n\nThe ring remains '
            'in your collection.',
        )


class DivorceView(DecisionView):
    def __init__(self, cog, owner_id, record):
        super().__init__(cog, owner_id)
        self.record = record

    @discord.ui.button(
        label='Confirm Divorce',
        emoji='🥀',
        style=discord.ButtonStyle.danger,
    )
    async def confirm(self, interaction, button):
        if self.finished:
            return await interaction.response.send_message(
                'This decision is closed.',
                ephemeral=True,
            )
        if not delete_marriage(interaction.guild.id, self.record):
            return await self.finish(
                interaction,
                'A LOST BOND',
                'This marriage no longer exists.',
            )
        await self.finish(
            interaction,
            'BROKEN BOND',
            '*Maybe you reached your limits...*',
        )
        await self.cog.sync_roles(interaction.guild, self.record[:2])

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction, button):
        await self.finish(
            interaction,
            'A BOND PRESERVED',
            'Your marriage remains intact.',
        )


class Marriage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        self.refresh_roles.start()

    def cog_unload(self):
        self.refresh_roles.cancel()

    def embed(self, title, description):
        embed = discord.Embed(
            title=f"✦ ───── {title} ───── ✦",
            description=f"\u200b\n{description}\n\u200b",
            color=0x74459A,
        )

        embed.set_image(url="attachment://divider1.gif")

        embed.set_footer(
            text=FOOTER,
            icon_url=self.bot.user.display_avatar.url,
        )

        return embed

    async def send(
        self, ctx, title, description, view=None, thumbnail=None
    ):
        embed = self.embed(title, description)

        files = [
            discord.File(GIF_PATH, filename="divider1.gif")
        ]

        if thumbnail:
            embed.set_thumbnail(url=thumbnail)

        elif LOVE_GIFS:
            love_gif = random.choice(LOVE_GIFS)

            embed.set_thumbnail(
                url=f"attachment://{love_gif.name}"
            )

            files.append(
                discord.File(love_gif, filename=love_gif.name)
            )

        message = await ctx.send(
            embed=embed,
            view=view,
            files=files,
        )

        if view:
            view.message = message

        return message

    async def sync_roles(self, guild, user_ids):
        names = {entry[1] for entry in LEVELS}
        for user_id in user_ids:
            member = guild.get_member(user_id)
            if member is None:
                continue
            record = get_marriage(guild.id, user_id)
            desired = marriage_level(record)[1][1] if record else None
            target = (
                discord.utils.get(guild.roles, name=desired)
                if desired else None
            )
            old = [
                role for role in member.roles
                if role.name in names and role != target
            ]
            try:
                if old:
                    await member.remove_roles(
                        *old,
                        reason='Marriage level update',
                    )
                if target and target not in member.roles:
                    await member.add_roles(
                        target,
                        reason='Marriage level update',
                    )
            except discord.HTTPException:
                LOG.warning(
                    'Could not update marriage roles for %s in %s',
                    user_id,
                    guild.id,
                )

    @tasks.loop(minutes=10)
    async def refresh_roles(self):
        with sqlite3.connect(DB_PATH, timeout=10) as db:
            records = db.execute(
                'SELECT guild_id, user_one, user_two FROM marriages'
            ).fetchall()
        for guild_id, first, second in records:
            guild = self.bot.get_guild(guild_id)
            if guild:
                await self.sync_roles(guild, (first, second))

    @refresh_roles.before_loop
    async def before_refresh(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.sync_roles(member.guild, (member.id,))

    @commands.command(name='propose')
    @commands.guild_only()
    async def propose(self, ctx, member: discord.Member):
        if member.id == ctx.author.id or member.bot:
            return await self.send(
                ctx,
                'FORBIDDEN PROMISE',
                'Choose another human member. Bot marriages require an '
                'administrator.',
            )
        if any(
            get_marriage(ctx.guild.id, m.id)
            for m in (ctx.author, member)
        ):
            return await self.send(
                ctx,
                'FORBIDDEN PROMISE',
                'One of you is already married.',
            )
        if not has_ring(ctx.guild.id, ctx.author.id):
            return await self.send(
                ctx,
                'MISSING RING',
                'Purchase an Engagement Ring with `$buy engagement_ring` '
                'first, buddy.',
            )
        view = ProposalView(self, ctx.author, member)
        await self.send(
            ctx,
            'A PROPOSAL',
            f'{ctx.author.mention} offers {member.mention} an engagement '
            f'ring.\n\n*Will you accept this bond?*',
            view=view,
            thumbnail=member.display_avatar.url,
        )

    @commands.command(name='marriage')
    @commands.guild_only()
    async def marriage(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        record = get_marriage(ctx.guild.id, member.id)
        if not record:
            return await self.send(
                ctx,
                'UNBOUNDED',
                f'{member.mention} is not married.',
            )
        first, second, married_at = record
        days, (_, name, emoji) = marriage_level(record)
        next_level = (
            'In Love — 7 days' if days < 7
            else 'Soulmates — 30 days' if days < 30
            else 'Maximum level reached'
        )
        await self.send(
            ctx,
            'LOVE IS IN THE AIR',
            f'<@{first}> & <@{second}>\n\n'
            f'☾ **Marriage Level:** {emoji} {name}\n'
            f'☾ **Married Since:** <t:{married_at // 10**9}:D>\n'
            f'☾ **Days Together:** {days}\n'
            f'☾ **Next Level:** {next_level}\n\n'
            '*Hope you stay together.*',
            thumbnail=member.display_avatar.url,
        )
        await self.sync_roles(ctx.guild, (first, second))

    @commands.command(name='divorce')
    @commands.guild_only()
    async def divorce(self, ctx):
        record = get_marriage(ctx.guild.id, ctx.author.id)
        if not record:
            return await self.send(
                ctx,
                'UNBOUNDED',
                'You are not married, yet.',
            )
        await self.send(
            ctx,
            'BROKEN BOND',
            'Are you certain you wish to end your marriage?',
            view=DivorceView(self, ctx.author.id, record),
        )

    @commands.command(name='adminmarry')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def admin_marry(
        self, ctx, first: discord.Member, second: discord.Member
    ):
        if not (first.bot or second.bot):
            return await self.send(
                ctx,
                'FORBIDDEN',
                'Human couples must use `$propose`.',
            )
        status = create_marriage(
            ctx.guild.id,
            first.id,
            second.id,
            consume_ring=False,
        )
        if status != 'success':
            return await self.send(
                ctx,
                'FORBIDDEN',
                'Choose two distinct, unmarried members.',
            )
        await self.send(
            ctx,
            'BONDED',
            f'{first.mention} and {second.mention} are now married.\n\n*You'
            f' cannot save yourself from the administrator.*',
        )
        await self.sync_roles(ctx.guild, (first.id, second.id))


async def setup(bot):
    create_marriage_database()
    await bot.add_cog(Marriage(bot))
