
import random
import sqlite3
import time
from pathlib import Path

import discord
from discord.ext import commands

DB_PATH = (
    Path(__file__).resolve().parent.parent
    / "data" / "olrox.db"
)


def create_database():
    """Create the experience table if it does not exist."""
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS experience (
                guild_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                xp INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (guild_id, user_id)
            )
            """
        )


def add_experience(guild_id, user_id, amount):
    """Add experience points to a server member."""
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            INSERT INTO experience (guild_id, user_id, xp)
            VALUES (?, ?, ?)
            ON CONFLICT(guild_id, user_id)
            DO UPDATE SET xp = xp + excluded.xp
            """,
            (guild_id, user_id, amount)
        )


def get_experience(guild_id, user_id):
    """Retrieve a member's experience points."""
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute(
            """
            SELECT xp
            FROM experience
            WHERE guild_id = ? AND user_id = ?
            """,
            (guild_id, user_id)
        )

        result = cursor.fetchone()

        if result is None:
            return 0

        return result[0]


def get_leaderboard(guild_id):
    """Retrieve the ten members with the most XP."""
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute(
            """
            SELECT user_id, xp
            FROM experience
            WHERE guild_id = ?
            ORDER BY xp DESC, user_id ASC
            LIMIT 10
            """,
            (guild_id,)
        )

        return cursor.fetchall()


class Levels(commands.Cog):
    """Manage experience and ranks."""

    def __init__(self, bot):
        self.bot = bot
        create_database()
        self.xp_cooldowns = {}

    @commands.command(name="rank")
    @commands.guild_only()
    async def rank(self, ctx, member: discord.Member = None):
        """Display a member's experience points."""
        if member is None:
            member = ctx.author

        xp = get_experience(
            ctx.guild.id,
            member.id
        )

        embed = discord.Embed(
            title="✦ ───── RANKING ───── ✦",
            description=(
                f"☾ **Member:** {member.display_name}\n"
                f"☾ **Experience:** {xp} XP\n"
                "*At least you're trying.*"
            ),
            color=0x74459A
        )

        embed.set_footer(
            text="THE REAL OLROX • Richter's childhood nightmare.",
            icon_url=member.display_avatar.url
        )

        image = discord.File(
            "assets/gifs/of_course.gif",
            filename="of_course.gif"
        )

        divider = discord.File(
            "assets/gifs/divider3.gif",
            filename="divider3.gif"
        )

        embed.set_thumbnail(
            url="attachment://of_course.gif"
        )

        embed.set_image(
            url="attachment://divider3.gif"
        )

        await ctx.send(embed=embed, files=[image, divider])

    @commands.command(name="addxp")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def addxp(
        self,
        ctx,
        member: discord.Member,
        amount: int
    ):
        """Give experience points to a server member."""
        if amount <= 0:
            await ctx.send(
                "Experience must be greater than zero."
            )
            return

        add_experience(
            ctx.guild.id,
            member.id,
            amount
        )

        total_xp = get_experience(
            ctx.guild.id,
            member.id
        )

        embed = discord.Embed(
            title="✦ ───── EXPERIENCE GRANTED ───── ✦",
            description=(
                f"☾ **Member:** {member.mention}\n"
                f"☾ **XP added:** +{amount}\n"
                f"☾ **Total experience:** {total_xp} XP\n\n"
                "*A little progress. How fascinating.*"
            ),
            color=0x74459A
        )

        image = discord.File(
            "assets/gifs/olrox2.gif",
            filename="olrox2.gif"
        )

        divider = discord.File(
            "assets/gifs/divider1.gif",
            filename="divider1.gif"
        )

        embed.set_thumbnail(
            url="attachment://olrox2.gif"
        )

        embed.set_image(
            url="attachment://divider1.gif"
        )

        embed.set_footer(
            text="THE REAL OLROX • Richter's childhood nightmare.",
            icon_url=self.bot.user.display_avatar.url
        )

        await ctx.send(
            embed=embed,
            files=[image, divider]
        )

    @commands.command(name="leaderboard", aliases=["top"])
    @commands.guild_only()
    async def leaderboard(self, ctx):
        """Display the ten members with the most XP."""
        ranking = get_leaderboard(ctx.guild.id)

        if not ranking:
            description = (
                "No experience has been recorded yet.\n\n"
                "*How terribly disappointing.*"
            )
        else:
            positions = []

            for position, (user_id, xp) in enumerate(
                ranking, start=1
            ):
                member = ctx.guild.get_member(user_id)

                if member:
                    name = discord.utils.escape_markdown(
                        member.display_name
                    )
                else:
                    name = f"User {user_id}"

                positions.append(
                    f"☾ **{position}.** {name} — **{xp} XP**"
                )

            description = "\n".join(positions)

        embed = discord.Embed(
            title="✦ ───── LEADERBOARD ───── ✦",
            description=description,
            color=0x74459A
        )

        image = discord.File(
            "assets/gifs/laugh.gif",
            filename="laugh.gif"
        )

        divider = discord.File(
            "assets/gifs/divider5.gif",
            filename="divider5.gif"
        )

        embed.set_thumbnail(
            url="attachment://laugh.gif"
        )

        embed.set_image(
            url="attachment://divider5.gif"
        )

        embed.set_footer(
            text="THE REAL OLROX • Richter's childhood nightmare.",
            icon_url=self.bot.user.display_avatar.url
        )

        await ctx.send(
            embed=embed,
            files=[image, divider]
        )

    @commands.Cog.listener()
    async def on_message(self, message):
        """Award XP for regular server activity."""
        if message.author.bot:
            return

        if message.guild is None:
            return

        if message.content.startswith("$"):
            return

        guild_id = message.guild.id
        user_id = message.author.id
        user_key = (guild_id, user_id)

        current_time = time.monotonic()
        last_message = self.xp_cooldowns.get(user_key, 0)

        if current_time - last_message < 60:
            return

        amount = random.randint(5, 15)

        add_experience(
            guild_id,
            user_id,
            amount
        )

        self.xp_cooldowns[user_key] = current_time



async def setup(bot):
    """Register the levels Cog."""
    await bot.add_cog(Levels(bot))
