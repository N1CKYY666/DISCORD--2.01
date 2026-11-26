
"""Profession and employment system for The Real Olrox."""

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

JOBS = {
    "baker": {
        "name": "Baker",
        "level": 1,
        "min_pay": 30,
        "max_pay": 65,
        "mission_type": "standard"
    },
    "gravedigger": {
        "name": "Gravedigger",
        "level": 1,
        "min_pay": 35,
        "max_pay": 80,
        "mission_type": "standard"
    },
    "merchant": {
        "name": "Merchant",
        "level": 3,
        "min_pay": 50,
        "max_pay": 100,
        "mission_type": "standard"
    },
    "speaker": {
        "name": "Speaker Apprentice",
        "level": 5,
        "min_pay": 65,
        "max_pay": 125,
        "mission_type": "standard"
    },
    "apothecary": {
        "name": "Apothecary",
        "level": 8,
        "min_pay": 85,
        "max_pay": 155,
        "mission_type": "standard"
    },
    "forgemaster": {
        "name": "Devil Forgemaster",
        "level": 10,
        "min_pay": 100,
        "max_pay": 180,
        "mission_type": "standard"
    },
    "revolutionary": {
        "name": "Revolutionary",
        "level": 12,
        "min_pay": 125,
        "max_pay": 210,
        "mission_type": "interactive"
    },
    "knight": {
        "name": "Knight of Saint John",
        "level": 15,
        "min_pay": 150,
        "max_pay": 240,
        "mission_type": "interactive"
    },
    "informant": {
        "name": "Vampire Informant",
        "level": 20,
        "min_pay": 175,
        "max_pay": 285,
        "mission_type": "interactive"
    },
    "hunter": {
        "name": "Vampire Hunter",
        "level": 25,
        "min_pay": 200,
        "max_pay": 320,
        "mission_type": "interactive"
    },
    "summoner": {
        "name": "Summoner",
        "level": 35,
        "min_pay": 275,
        "max_pay": 425,
        "mission_type": "elite"
    },
    "lieutenant": {
        "name": "Vampire Lieutenant",
        "level": 50,
        "min_pay": 400,
        "max_pay": 600,
        "mission_type": "elite"
    }
}

JOB_EMOJIS = {
    "baker": "<:trigo:1573507229817118720>",
    "gravedigger": "<:pala:1573507368497709108>",
    "speaker": "<:speakers:1573507308192010300>",
    "knight": "<:saint_john:1573500680608546897>",
    "forgemaster": "<:forgemaster:1573508322831761488>",
    "hunter": "<:belmont:1573216480823345182>",
    "lieutenant": "<:eclipse:1573737278331953162>",
    "merchant": "<:balance:1573769035806539846>",
    "apothecary": "<:alquimist:1573770637074497656>",
    "revolutionary": "<:frigio:1573770685569040544>",
    "informant": "<:envelope1:1573770919011287211>",
    "summoner": "<:summoner:1573767607792701490>",
}


def job_command(job):
    return "$work" if job["mission_type"] == "standard" else "$mission"


def job_pay(job):
    if job["mission_type"] == "standard":
        return f"{job['min_pay']}–{job['max_pay']} Livres"
    if job["mission_type"] == "elite":
        return "Louis d'or (coming soon)"
    return "Mission-based · Livres"


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

        active = connection.execute(
            "SELECT expires_at FROM active_missions "
            "WHERE guild_id = ? AND user_id = ?",
            (guild_id, user_id)
        ).fetchone()
        if active and active[0] > now:
            return "active_mission", active[0] - now

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
                "Apply for your own job. Use `$jobs`.",
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

    @commands.command(name="testjob", hidden=True)
    @commands.guild_only()
    @commands.is_owner()
    async def testjob(self, ctx, profession: str = None):
        """Temporarily bypass job restrictions for bot testing."""
        if profession is None:
            await ctx.send(
                "Specify a profession\n"
                "Example: `$testjob revolutionary`."
            )
            return

        profession = profession.lower().strip()

        if profession not in JOBS:
            await ctx.send(
                "That profession doesn't exist.\n"
                "Consult `$jobs`."
            )
            return

        now = int(time.time())

        with sqlite3.connect(DB_PATH, timeout=10) as connection:
            connection.execute("BEGIN IMMEDIATE")

            connection.execute(
                """
                INSERT INTO user_jobs (
                    guild_id,
                    user_id,
                    job_id,
                    last_change
                )
                VALUES (?, ?, ?, ?)
                ON CONFLICT(guild_id, user_id)
                DO UPDATE SET
                    job_id = excluded.job_id,
                    last_change = excluded.last_change
                """,
                (
                    ctx.guild.id,
                    ctx.author.id,
                    profession,
                    now
                )
            )

        job = JOBS[profession]
        emoji = JOB_EMOJIS.get(profession, "◈")

        embed = discord.Embed(
            title="✦ ───── TEST CONTRACT ───── ✦",
            description=(
                f"{emoji} **{job['name']}**\n\n"
                "Your profession has been changed "
                "for testing purposes.\n\n"
                "◈ **Contract cooldown:** Bypassed\n"
                "◈ **Required level:** Bypassed\n\n"
                "*Try not to abuse your privileges.*"
            ),
            color=0x74459A
        )

        embed.set_footer(
            text="THE REAL OLROX • Developer access."
        )

        await ctx.send(embed=embed)

    @commands.command(name="testreset", hidden=True)
    @commands.guild_only()
    @commands.is_owner()
    async def testreset(self, ctx):
        """Reset the owner's work cooldown for testing."""
        with sqlite3.connect(DB_PATH, timeout=10) as connection:
            connection.execute("BEGIN IMMEDIATE")

            connection.execute(
                """
                UPDATE user_jobs
                SET last_work = 0
                WHERE guild_id = ? AND user_id = ?
                """,
                (ctx.guild.id, ctx.author.id)
            )

            connection.execute(
                """
                DELETE FROM active_missions
                WHERE guild_id = ? AND user_id = ?
                """,
                (ctx.guild.id, ctx.author.id)
            )

        embed = discord.Embed(
            title="✦ ───── TEST RESET ───── ✦",
            description=(
                "Your work cooldown has been reset.\n\n"
                "◈ **Work cooldown:** Cleared\n"
                "◈ **Pending mission:** Cancelled\n\n"
                "*The revolution waits for no one*"
            ),
            color=0x74459A
        )

        embed.set_footer(
            text="THE REAL OLROX • Developer access."
        )

        await ctx.send(embed=embed)

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
                    f"{job_pay(job)}\n"
                    f"Command: `{job_command(job)}` · ID: `{job_id}`\n"
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
                "A profession. Try `$jobs` first."
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

        if status == "active_mission":
            await ctx.send("Finish your current assignment first.")
            return

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
                f"**{job['name']}**."
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
                f"{job_pay(job)}\n"
                f"◈ **Command:** `{job_command(job)}`\n"
                "◈ **Shift cooldown:** 30 minutes\n"
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


async def setup(bot):
    """Register the jobs Cog."""
    await bot.add_cog(Jobs(bot))
