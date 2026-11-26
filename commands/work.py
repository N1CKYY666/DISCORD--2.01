"""Paid shifts for The Real Olrox."""

import random
import sqlite3
import time
from pathlib import Path

import discord
from discord.ext import commands

from commands.jobs import DB_PATH, JOB_EMOJIS, JOBS
from commands.levels import calculate_level

WORK_COOLDOWN = 30 * 60
GIF_DIR = Path(__file__).resolve().parent.parent / "assets" / "gifs"
WORK_THUMBNAILS = (
    GIF_DIR / "apologies.gif",
    GIF_DIR / "cute_baby.jpg",
)


def perform_work(guild_id, user_id):
    """Pay a worker and enforce the 30-minute cooldown."""
    now = int(time.time())

    with sqlite3.connect(DB_PATH, timeout=10) as connection:
        connection.execute("BEGIN IMMEDIATE")

        result = connection.execute(
            """
            SELECT job_id, last_work
            FROM user_jobs
            WHERE guild_id = ? AND user_id = ?
            """,
            (guild_id, user_id)
        ).fetchone()

        if result is None:
            return "unemployed", None, 0

        job_id, last_work = result
        job = JOBS.get(job_id)

        if job is None:
            return "invalid_job", None, 0

        if job["mission_type"] != "standard":
            return "use_mission", job_id, 0

        mission_remaining = check_active_mission(
            connection, guild_id, user_id, now
        )
        if mission_remaining > 0:
            return "active_mission", job_id, mission_remaining

        remaining = WORK_COOLDOWN - (now - last_work)

        if remaining > 0:
            return "cooldown", job_id, remaining

        salary = random.randint(
            job["min_pay"],
            job["max_pay"]
        )

        connection.execute(
            """
            INSERT OR IGNORE INTO economy (
                guild_id, user_id
            )
            VALUES (?, ?)
            """,
            (guild_id, user_id)
        )

        connection.execute(
            """
            UPDATE economy
            SET balance = balance + ?
            WHERE guild_id = ? AND user_id = ?
            """,
            (salary, guild_id, user_id)
        )

        connection.execute(
            """
            UPDATE user_jobs
            SET last_work = ?
            WHERE guild_id = ? AND user_id = ?
            """,
            (now, guild_id, user_id)
        )

        return "success", job_id, salary


def check_active_mission(connection, guild_id, user_id, now):
    """Check for a pending mission and clear expired reservations."""
    result = connection.execute(
        """
        SELECT expires_at
        FROM active_missions
        WHERE guild_id = ? AND user_id = ?
        """,
        (guild_id, user_id)
    ).fetchone()

    if result is None:
        return 0

    remaining = result[0] - now

    if remaining > 0:
        return remaining

    connection.execute(
        """
        DELETE FROM active_missions
        WHERE guild_id = ? AND user_id = ?
        """,
        (guild_id, user_id)
    )

    return 0


def perform_random_work(guild_id, user_id):
    """Complete a random job without changing the main profession."""
    now = int(time.time())

    with sqlite3.connect(DB_PATH, timeout=10) as connection:
        connection.execute("BEGIN IMMEDIATE")
        mission_remaining = check_active_mission(
            connection, guild_id, user_id, now
        )

        if mission_remaining > 0:
            return "active_mission", None, mission_remaining

        result = connection.execute(
            """
            SELECT job_id, last_work
            FROM user_jobs
            WHERE guild_id = ? AND user_id = ?
            """,
            (guild_id, user_id)
        ).fetchone()

        if result is None:
            return "unemployed", None, 0

        current_job, last_work = result

        if current_job not in JOBS:
            return "invalid_job", None, 0

        remaining = WORK_COOLDOWN - (now - last_work)

        if remaining > 0:
            return "cooldown", current_job, remaining

        xp_result = connection.execute(
            """
            SELECT xp
            FROM experience
            WHERE guild_id = ? AND user_id = ?
            """,
            (guild_id, user_id)
        ).fetchone()

        user_xp = xp_result[0] if xp_result else 0
        user_level, _, _ = calculate_level(user_xp)

        available_jobs = [
            job_id
            for job_id, job in JOBS.items()
            if user_level >= job["level"]
            and job["mission_type"] == "standard"
        ]

        if not available_jobs:
            return "no_jobs", None, 0

        random_job_id = random.choice(available_jobs)
        job = JOBS[random_job_id]

        salary = random.randint(
            job["min_pay"],
            job["max_pay"]
        )

        connection.execute(
            """
            INSERT OR IGNORE INTO economy (guild_id, user_id)
            VALUES (?, ?)
            """,
            (guild_id, user_id)
        )

        connection.execute(
            """
            UPDATE economy
            SET balance = balance + ?
            WHERE guild_id = ? AND user_id = ?
            """,
            (salary, guild_id, user_id)
        )

        connection.execute(
            """
            UPDATE user_jobs
            SET last_work = ?
            WHERE guild_id = ? AND user_id = ?
            """,
            (now, guild_id, user_id)
        )

        return "success", random_job_id, salary


def pay_mission_reward(guild_id, user_id, job_id, reward):
    """Pay a completed mission and enforce the shared cooldown."""
    now = int(time.time())

    with sqlite3.connect(DB_PATH, timeout=10) as connection:
        connection.execute("BEGIN IMMEDIATE")
        mission_remaining = check_active_mission(
            connection, guild_id, user_id, now
        )

        if mission_remaining > 0:
            return "active_mission", None, mission_remaining

        result = connection.execute(
            """
            SELECT job_id, last_work
            FROM user_jobs
            WHERE guild_id = ? AND user_id = ?
            """,
            (guild_id, user_id)
        ).fetchone()

        if result is None:
            return "unemployed", 0

        current_job, last_work = result

        if current_job != job_id:
            return "wrong_job", 0

        remaining = WORK_COOLDOWN - (now - last_work)

        if remaining > 0:
            return "cooldown", remaining

        if not isinstance(reward, int) or reward < 0:
            return "invalid_reward", 0

        connection.execute(
            """
            INSERT OR IGNORE INTO economy (guild_id, user_id)
            VALUES (?, ?)
            """,
            (guild_id, user_id)
        )

        connection.execute(
            """
            UPDATE economy
            SET balance = balance + ?
            WHERE guild_id = ? AND user_id = ?
            """,
            (reward, guild_id, user_id)
        )

        connection.execute(
            """
            UPDATE user_jobs
            SET last_work = ?
            WHERE guild_id = ? AND user_id = ?
            """,
            (now, guild_id, user_id)
        )

        return "success", reward


class Work(commands.Cog):
    """Manage paid shifts and random work."""

    def __init__(self, bot):
        self.bot = bot

    async def send_work_embed(self, ctx, title, description):
        """Send a work response with the shared visual style."""
        embed = discord.Embed(
            title=title,
            description=description,
            color=0x74459A
        )
        thumbnails = [path for path in WORK_THUMBNAILS if path.is_file()]
        files = []

        if thumbnails:
            thumbnail = random.choice(thumbnails)
            embed.set_thumbnail(url=f"attachment://{thumbnail.name}")
            files.append(discord.File(thumbnail, filename=thumbnail.name))

        divider = GIF_DIR / "divider1.gif"
        embed.set_image(url="attachment://divider1.gif")
        files.append(discord.File(divider, filename="divider1.gif"))
        embed.set_footer(
            text="THE REAL OLROX • Working hard.",
            icon_url=self.bot.user.display_avatar.url
        )
        await ctx.send(embed=embed, files=files)

    @commands.command(name="work")
    @commands.guild_only()
    async def work(self, ctx, mode: str = None):
        """Work in the main profession or a random unlocked job."""
        if mode is not None and mode.lower() != "random":
            await self.send_work_embed(
                ctx,
                "✦ ───── UNKNOWN WORK ───── ✦",
                "Unknown work mode.\n"
                "Use `$work` or `$work random`."
            )
            return

        is_random = mode is not None

        if is_random:
            status, job_id, result = perform_random_work(
                ctx.guild.id,
                ctx.author.id
            )
        else:
            status, job_id, result = perform_work(
                ctx.guild.id,
                ctx.author.id
            )

        if status == "use_mission":
            job = JOBS[job_id]
            await self.send_work_embed(
                ctx,
                "✦ ───── A NEW PURPOSE ───── ✦",
                (
                    f"As a **{job['name']}**, your duties require "
                    "more than ordinary labor.\n\n"
                    "Use `$mission` for your next assignment.\n"
                    "Use `$work random` for an ordinary paid shift."
                )
            )
            return

        if status == "active_mission":
            await self.send_work_embed(
                ctx,
                "✦ ───── ACTIVE ASSIGNMENT ───── ✦",
                "You're already on an assignment, dear.\n"
                f"Finish it or wait **{result} seconds** "
                "before accepting another shift."
            )
            return

        if status == "unemployed":
            await self.send_work_embed(
                ctx,
                "✦ ───── UNEMPLOYED ───── ✦",
                "Unemployed? How unfortunate.\n"
                "Browse `$jobs` and choose a profession "
                "with `$job <profession>`."
            )
            return

        if status == "invalid_job":
            await self.send_work_embed(
                ctx,
                "✦ ───── INVALID CONTRACT ───── ✦",
                "Your employment records appear to be corrupted. "
                "How embarrassing."
            )
            return

        if status == "no_jobs":
            await self.send_work_embed(
                ctx,
                "✦ ───── NO AVAILABLE JOBS ───── ✦",
                "No professions are available at your level."
            )
            return

        job = JOBS[job_id]
        emoji = JOB_EMOJIS.get(job_id, "◈")
        livre_emoji = "<:livre:1573206463147544586>"

        if status == "cooldown":
            minutes, seconds = divmod(result, 60)

            title = "✦ ───── ON BREAK ───── ✦"
            description = (
                "You've already completed your shift.\n\n"
                f"◈ **Next shift:** {minutes}m {seconds}s\n\n"
                "*Get some rest.*"
            )
        else:
            title = (
                "✦ ─── RANDOM SHIFT ─── ✦"
                if is_random
                else "✦ ───── SHIFT COMPLETED ───── ✦"
            )

            description = (
                f"☾ **Employee:** {ctx.author.mention}\n\n"
                f"{emoji} **Profession:** {job['name']}\n"
                f"{livre_emoji} **Earned:** +{result:,} Livres\n\n"
                "◈ **Next shift:** 30 minutes\n\n"
                "*Your labor has been... adequate.*"
            )

        await self.send_work_embed(ctx, title, description)



async def setup(bot):
    """Register the work Cog."""
    await bot.add_cog(Work(bot))
