
"""Profession and employment system for The Real Olrox."""

import random
import sqlite3
import time
from pathlib import Path

import discord
from discord.ext import commands

from commands.levels import calculate_level

DB_PATH = (
    Path(__file__).resolve().parent.parent
    / "data" / "olrox.db"
)

JOB_CHANGE_COOLDOWN = 24 * 60 * 60
WORK_COOLDOWN = 30 * 60

JOBS = {
    "baker": {
        "name": "Baker",
        "level": 1,
        "min_pay": 30,
        "max_pay": 65
    },
    "gravedigger": {
        "name": "Gravedigger",
        "level": 1,
        "min_pay": 35,
        "max_pay": 80
    },
    "speaker": {
        "name": "Speaker Apprentice",
        "level": 5,
        "min_pay": 65,
        "max_pay": 125
    },
    "knight": {
        "name": "Knight of Saint John",
        "level": 15,
        "min_pay": 150,
        "max_pay": 240
    },
    "forgemaster": {
        "name": "Devil Forgemaster",
        "level": 10,
        "min_pay": 100,
        "max_pay": 180
    },
    "hunter": {
        "name": "Vampire Hunter",
        "level": 25,
        "min_pay": 200,
        "max_pay": 320
    }
}

JOB_EMOJIS = {
    "baker": "<:trigo:1573507229817118720>",
    "gravedigger": "<:pala:1573507368497709108>",
    "speaker": "<:speakers:1573507308192010300>",
    "knight": "<:saint_john:1573500680608546897>",
    "forgemaster": "<:forgemaster:1573508322831761488>",
    "hunter": "<:belmont:1573216480823345182>"
}


def select_job(guild_id, user_id, job_id):
    """Select a profession with a 24-hour change cooldown."""
    now = int(time.time())

    with sqlite3.connect(DB_PATH, timeout=10) as connection:
        connection.execute("BEGIN IMMEDIATE")

        result = connection.execute(
            """
            SELECT job_id, last_change
            FROM user_jobs
            WHERE guild_id = ? AND user_id = ?
            """,
            (guild_id, user_id)
        ).fetchone()

        if result is None:
            connection.execute(
                """
                INSERT INTO user_jobs (
                    guild_id, user_id, job_id, last_change
                )
                VALUES (?, ?, ?, ?)
                """,
                (guild_id, user_id, job_id, now)
            )
            return "selected", 0

        current_job, last_change = result

        if current_job == job_id:
            return "same", 0

        remaining = JOB_CHANGE_COOLDOWN - (now - last_change)

        if remaining > 0:
            return "cooldown", remaining

        connection.execute(
            """
            UPDATE user_jobs
            SET job_id = ?, last_change = ?
            WHERE guild_id = ? AND user_id = ?
            """,
            (job_id, now, guild_id, user_id)
        )

        return "changed", 0


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


def perform_random_work(guild_id, user_id):
    """Complete a random job without changing the main profession."""
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


class JobsView(discord.ui.View):
    """Navigate between profession catalog pages."""

    def __init__(self, author_id, pages):
        super().__init__(timeout=180)
        self.author_id = author_id
        self.pages = pages
        self.current_page = 0
        self.update_buttons()

    def update_buttons(self):
        self.previous_button.disabled = self.current_page == 0
        self.next_button.disabled = (
            self.current_page == len(self.pages) - 1
        )

    async def interaction_check(self, interaction):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "Apply for your own job, darling. Use `$jobs`.",
                ephemeral=True
            )
            return False

        return True

    @discord.ui.button(
        label="Previous",
        emoji="◀️",
        style=discord.ButtonStyle.secondary
    )
    async def previous_button(self, interaction, button):
        self.current_page -= 1
        self.update_buttons()

        await interaction.response.edit_message(
            embed=self.pages[self.current_page],
            view=self
        )

    @discord.ui.button(
        label="Next",
        emoji="▶️",
        style=discord.ButtonStyle.secondary
    )
    async def next_button(self, interaction, button):
        self.current_page += 1
        self.update_buttons()

        await interaction.response.edit_message(
            embed=self.pages[self.current_page],
            view=self
        )

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True


class Jobs(commands.Cog):
    """Manage professions, contracts, and employment."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="jobs")
    @commands.guild_only()
    async def jobs(self, ctx):
        """Display an interactive profession catalog."""
        with sqlite3.connect(DB_PATH) as connection:
            result = connection.execute(
                """
                SELECT xp
                FROM experience
                WHERE guild_id = ? AND user_id = ?
                """,
                (ctx.guild.id, ctx.author.id)
            ).fetchone()

        user_xp = result[0] if result else 0
        user_level, _, _ = calculate_level(user_xp)

        job_items = list(JOBS.items())
        pages = []

        for start in range(0, len(job_items), 3):
            job_list = []

            for job_id, job in job_items[start:start + 3]:
                emoji = JOB_EMOJIS.get(job_id, "◈")
                unlocked = user_level >= job["level"]
                status = "✧ Available" if unlocked else "⊘ Locked"

                job_list.append(
                    f"{emoji} **{job['name']}**\n"
                    f"Level {job['level']} · "
                    f"{job['min_pay']}–{job['max_pay']} Livres\n"
                    f"**{status}**"
                )

            page_number = len(pages) + 1
            total_pages = (len(job_items) + 2) // 3

            embed = discord.Embed(
                title="# ✦ ───── JOB APPLICATION ───── ✦",
                description=(
                    "☾ **Available Professions**\n"
                    f"**Your Level:** {user_level}\n\n"
                    + "\n\n".join(job_list)
                    + "\n\n"
                    "*Even the aristocracy must earn its keep.*"
                ),
                color=0x74459A
            )

            embed.set_thumbnail(
                url="attachment://shine.gif"
            )

            embed.set_image(
                url="attachment://divider1.gif"
            )

            embed.set_footer(
                text=(
                    "THE REAL OLROX • "
                    "Richter's childhood nightmare. "
                    f"• Page {page_number}/{total_pages}"
                ),
                icon_url=self.bot.user.display_avatar.url
            )

            pages.append(embed)

        view = JobsView(ctx.author.id, pages)

        image = discord.File(
            "assets/gifs/shine.gif",
            filename="shine.gif"
        )

        divider = discord.File(
            "assets/gifs/divider1.gif",
            filename="divider1.gif"
        )

        message = await ctx.send(
            embed=pages[0],
            files=[image, divider],
            view=view
        )

        view.message = message

    @commands.command(name="job")
    @commands.guild_only()
    async def job(self, ctx, profession: str = None):
        """Choose a primary profession."""
        if profession is None:
            await ctx.send(
                "A profession, darling. Try `$jobs` first."
            )
            return

        profession = profession.lower().strip()

        if profession not in JOBS:
            await ctx.send(
                "That profession doesn't exist. "
                "Consult `$jobs` before embarrassing yourself."
            )
            return

        job = JOBS[profession]

        with sqlite3.connect(DB_PATH) as connection:
            result = connection.execute(
                """
                SELECT xp
                FROM experience
                WHERE guild_id = ? AND user_id = ?
                """,
                (ctx.guild.id, ctx.author.id)
            ).fetchone()

        user_xp = result[0] if result else 0
        user_level, _, _ = calculate_level(user_xp)

        if user_level < job["level"]:
            await ctx.send(
                f"**{job['name']}** requires level "
                f"**{job['level']}**.\n"
                f"You're only level **{user_level}**. "
                "Ambition is charming. Delusion, less so."
            )
            return

        status, remaining = select_job(
            ctx.guild.id,
            ctx.author.id,
            profession
        )

        if status == "cooldown":
            hours, remainder = divmod(remaining, 3600)
            minutes = remainder // 60

            await ctx.send(
                "Your current contract is still binding.\n"
                f"Try again in **{hours}h {minutes}m**."
            )
            return

        if status == "same":
            await ctx.send(
                f"You're already employed as "
                f"**{job['name']}**, darling."
            )
            return

        emoji = JOB_EMOJIS.get(profession, "◈")

        if status == "selected":
            message = (
                "Your application has been accepted.\n"
                "Try not to burn anything"
            )
        else:
            message = (
                "Your transfer has been approved.\n"
                "Do make yourself useful."
            )

        embed = discord.Embed(
            title="✦ ───── CONTRACT APPROVED ───── ✦",
            description=(
                f"{emoji} **{job['name']}**\n\n"
                f"{message}\n\n"
                f"◈ **Required Level:** {job['level']}\n"
                f"◈ **Salary:** "
                f"{job['min_pay']}–{job['max_pay']} Livres\n"
                "◈ **Contract Changes:** Every 24 hours"
            ),
            color=0x74459A
        )

        image = discord.File(
            "assets/gifs/nocturne.gif",
            filename="nocturne.gif"
        )

        divider = discord.File(
            "assets/gifs/divider1.gif",
            filename="divider1.gif"
        )

        embed.set_thumbnail(
            url="attachment://nocturne.gif"
        )

        embed.set_image(
            url="attachment://divider1.gif"
        )

        embed.set_footer(
            text=(
                "THE REAL OLROX • "
                "Richter's childhood nightmare."
            ),
            icon_url=self.bot.user.display_avatar.url
        )

        await ctx.send(
            embed=embed,
            files=[image, divider]
        )

    @commands.command(name="work")
    @commands.guild_only()
    async def work(self, ctx, mode: str = None):
        """Work in the main profession or a random unlocked job."""
        if mode is not None and mode.lower() != "random":
            await ctx.send(
                "Unknown work mode, darling.\n"
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

        if status == "unemployed":
            await ctx.send(
                "Unemployed? How unfortunate.\n"
                "Browse `$jobs` and choose a profession "
                "with `$job <profession>`."
            )
            return

        if status == "invalid_job":
            await ctx.send(
                "Your employment records appear to be corrupted. "
                "How embarrassing."
            )
            return

        if status == "no_jobs":
            await ctx.send(
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
                "✦ ─── RANDOM SHIFT COMPLETED ─── ✦"
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

        embed = discord.Embed(
            title=title,
            description=description,
            color=0x74459A
        )

        image = discord.File(
            "assets/gifs/apologies.gif",
            filename="apologies.gif"
        )

        divider = discord.File(
            "assets/gifs/divider1.gif",
            filename="divider1.gif"
        )

        embed.set_thumbnail(
            url="attachment://apologies.gif"
        )

        embed.set_image(
            url="attachment://divider1.gif"
        )

        embed.set_footer(
            text=(
                "THE REAL OLROX • "
                "Working hard."
            ),
            icon_url=self.bot.user.display_avatar.url
        )

        await ctx.send(
            embed=embed,
            files=[image, divider]
        )


async def setup(bot):
    """Register the jobs Cog."""
    await bot.add_cog(Jobs(bot))
