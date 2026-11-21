
import sqlite3
import time
from pathlib import Path

import discord
from discord.ext import commands

DB_PATH = (
    Path(__file__).resolve().parent.parent
    / "data" / "olrox.db"
)


def create_economy_database():
    """Create and update the economy database."""
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS economy (
                guild_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                balance INTEGER NOT NULL DEFAULT 0,
                louis_dor INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (guild_id, user_id)
            )
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS user_jobs (
                guild_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                job_id TEXT NOT NULL,
                last_change INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (guild_id, user_id)
            )
            """
        )

        # Check economy columns.
        economy_columns = {
            row[1]
            for row in connection.execute(
                "PRAGMA table_info(economy)"
            ).fetchall()
        }

        if "louis_dor" not in economy_columns:
            connection.execute(
                """
                ALTER TABLE economy
                ADD COLUMN louis_dor INTEGER NOT NULL DEFAULT 0
                """
            )

        if "last_daily" not in economy_columns:
            connection.execute(
                """
                ALTER TABLE economy
                ADD COLUMN last_daily INTEGER NOT NULL DEFAULT 0
                """
            )

        # Check user_jobs columns.
        job_columns = {
            row[1]
            for row in connection.execute(
                "PRAGMA table_info(user_jobs)"
            ).fetchall()
        }

        if "last_work" not in job_columns:
            connection.execute(
                """
                ALTER TABLE user_jobs
                ADD COLUMN last_work INTEGER NOT NULL DEFAULT 0
                """
            )


def get_balance(guild_id, user_id):
    """Retrieve a member's livres and louis d'or."""
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute(
            """
            SELECT balance, louis_dor
            FROM economy
            WHERE guild_id = ? AND user_id = ?
            """,
            (guild_id, user_id)
        )

        result = cursor.fetchone()

        if result is None:
            return 0, 0

        return result


DAILY_REWARD = 150
DAILY_COOLDOWN = 24 * 60 * 60


def claim_daily(guild_id, user_id):
    """Claim daily livres once every 24 hours."""
    now = int(time.time())

    with sqlite3.connect(DB_PATH, timeout=10) as connection:
        connection.execute("BEGIN IMMEDIATE")

        connection.execute(
            """
            INSERT OR IGNORE INTO economy (guild_id, user_id)
            VALUES (?, ?)
            """,
            (guild_id, user_id)
        )

        last_daily = connection.execute(
            """
            SELECT last_daily
            FROM economy
            WHERE guild_id = ? AND user_id = ?
            """,
            (guild_id, user_id)
        ).fetchone()[0]

        remaining = DAILY_COOLDOWN - (now - last_daily)

        if remaining > 0:
            return False, remaining

        connection.execute(
            """
            UPDATE economy
            SET balance = balance + ?,
                last_daily = ?
            WHERE guild_id = ? AND user_id = ?
            """,
            (DAILY_REWARD, now, guild_id, user_id)
        )

        return True, DAILY_REWARD


class Economy(commands.Cog):
    """Manage the server's virtual economy. wink wink"""

    def __init__(self, bot):
        self.bot = bot
        create_economy_database()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if ctx.command and ctx.command.cog is self:
            print(f"[ECONOMY ERROR] {error!r}")

    @commands.command(name="balance", aliases=["bal"])
    @commands.guild_only()
    async def balance(self, ctx, member: discord.Member = None):
        """Display a member's virtual coin balance."""
        if member is None:
            member = ctx.author

        livres, louis_dor = get_balance(
            ctx.guild.id,
            member.id
        )

        livre_emoji = "<:livre:1573206463147544586>"
        louis_emoji = "<:louis_dor:1573206641422377041>"

        embed = discord.Embed(
            title="✦ ───── ROYAL TREASURY ───── ✦",
            description=(
                f"☾ **Account Holder:** {member.mention}\n\n"
                "✦ ── **YOUR BALANCE** ── ✦\n\n"
                f"{livre_emoji} **Livres:** {livres:,}\n"
                f"{louis_emoji} **Louis D'or:** {louis_dor:,}\n\n"
                "*Try not to spend it all at once.*"
            ),
            color=0x74459A
        )

        image = discord.File(
            "assets/gifs/shine.gif",
            filename="shine.gif"
        )

        divider = discord.File(
            "assets/gifs/divider1.gif",
            filename="divider1.gif"
        )

        embed.set_thumbnail(
            url="attachment://shine.gif"
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

    @commands.command(name="daily")
    @commands.guild_only()
    async def daily(self, ctx):
        """Claim a daily reward of 150 livres."""
        success, result = claim_daily(
            ctx.guild.id,
            ctx.author.id
        )

        livre_emoji = "<:livre:1573206463147544586>"

        if success:
            embed = discord.Embed(
                title="✦ ───── YOUR ALLOWANCE ───── ✦",
                description=(
                    f"☾ **Account Holder:** {ctx.author.mention}\n\n"
                    f"{livre_emoji} **Reward:** +{result:,} Livres\n\n"
                    "*How generous of me. Have a good day.*"
                ),
                color=0x74459A
            )

        else:
            hours, remainder = divmod(result, 3600)
            minutes, seconds = divmod(remainder, 60)

            embed = discord.Embed(
                title="✦ ───── NOT SO FAST ───── ✦",
                description=(
                    f"☾ **Account Holder:** {ctx.author.mention}\n\n"
                    "You've already collected your allowance.\n\n"
                    f"◈ **Next claim:** "
                    f"{hours}h {minutes}m {seconds}s\n\n"
                    "*Patience. Useful virtue.*"
                ),
                color=0x74459A
            )

        image = discord.File(
            "assets/gifs/olrox3.gif",
            filename="olrox3.gif"
        )

        divider = discord.File(
            "assets/gifs/divider1.gif",
            filename="divider1.gif"
        )

        embed.set_thumbnail(
            url="attachment://olrox3.gif"
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


async def setup(bot):
    """Register the economy Cog."""
    await bot.add_cog(Economy(bot))
