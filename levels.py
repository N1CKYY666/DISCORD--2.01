
import sqlite3
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


class Levels(commands.Cog):
    """Manage experience and ranks."""

    def __init__(self, bot):
        self.bot = bot
        create_database()

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


async def setup(bot):
    """Register the levels Cog."""
    await bot.add_cog(Levels(bot))
