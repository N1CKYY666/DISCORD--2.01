"""Interactive mission interfaces for The Real Olrox."""

import random
import sqlite3
import time

import discord
from discord.ext import commands

from commands.jobs import DB_PATH
from commands.work import WORK_COOLDOWN


def get_revolutionary_mission():
    """Return the first Revolutionary mission."""
    return {
        "id": "supply_convoy",
        "title": "The Supply Convoy",
        "description": (
            "A royal convoy is transporting supplies "
            "through the countryside.\n"
            "Your allies desperately need those resources."
        ),
    }


def reserve_mission(guild_id, user_id, job_id, mission_id):
    """Reserve one mission without paying its reward."""
    now = int(time.time())
    expires_at = now + 60

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
            return "unemployed", 0

        current_job, last_work = result

        if current_job != job_id:
            return "wrong_job", 0

        remaining = WORK_COOLDOWN - (now - last_work)

        if remaining > 0:
            return "cooldown", remaining

        active = connection.execute(
            """
            SELECT expires_at
            FROM active_missions
            WHERE guild_id = ? AND user_id = ?
            """,
            (guild_id, user_id)
        ).fetchone()

        if active is not None:
            active_remaining = active[0] - now

            if active_remaining > 0:
                return "active_mission", active_remaining

            connection.execute(
                """
                DELETE FROM active_missions
                WHERE guild_id = ? AND user_id = ?
                """,
                (guild_id, user_id)
            )

        connection.execute(
            """
            INSERT INTO active_missions (
                guild_id,
                user_id,
                job_id,
                mission_id,
                expires_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                guild_id,
                user_id,
                job_id,
                mission_id,
                expires_at
            )
        )

        return "reserved", 60


def complete_mission(
    guild_id, user_id, job_id, mission_id, choice
):
    """Complete a mission and award its reward exactly once."""
    now = int(time.time())

    if (
        job_id != "revolutionary"
        or mission_id != "supply_convoy"
        or choice not in REVOLUTIONARY_REWARDS
    ):
        return "invalid_mission", 0, False

    with sqlite3.connect(DB_PATH, timeout=10) as connection:
        connection.execute("BEGIN IMMEDIATE")

        reservation = connection.execute(
            """
            SELECT job_id, mission_id, expires_at
            FROM active_missions
            WHERE guild_id = ? AND user_id = ?
            """,
            (guild_id, user_id)
        ).fetchone()

        if reservation is None:
            return "no_mission", 0, False

        reserved_job, reserved_mission, expires_at = reservation

        if now >= expires_at:
            connection.execute(
                """
                DELETE FROM active_missions
                WHERE guild_id = ? AND user_id = ?
                """,
                (guild_id, user_id)
            )
            return "expired", 0, False

        if (
            reserved_job != job_id
            or reserved_mission != mission_id
        ):
            return "wrong_mission", 0, False

        result = connection.execute(
            """
            SELECT job_id, last_work
            FROM user_jobs
            WHERE guild_id = ? AND user_id = ?
            """,
            (guild_id, user_id)
        ).fetchone()

        if result is None or result[0] != job_id:
            return "wrong_job", 0, False

        remaining = WORK_COOLDOWN - (now - result[1])

        if remaining > 0:
            return "cooldown", remaining, False

        settings = REVOLUTIONARY_REWARDS[choice]
        success = random.random() < settings["success_chance"]

        pay_range = (
            settings["success_pay"]
            if success
            else settings["failure_pay"]
        )

        reward = random.randint(*pay_range)

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

        connection.execute(
            """
            DELETE FROM active_missions
            WHERE guild_id = ? AND user_id = ?
            """,
            (guild_id, user_id)
        )

        return "success", reward, success


REVOLUTIONARY_REWARDS = {
    "stealth": {
        "success_chance": 0.80,
        "success_pay": (125, 180),
        "failure_pay": (25, 50),
    },
    "assault": {
        "success_chance": 0.55,
        "success_pay": (180, 250),
        "failure_pay": (0, 35),
    },
}


class MissionView(discord.ui.View):
    """Interactive mission with two possible strategies LMAOOO."""

    def __init__(
        self,
        author_id,
        guild_id=None,
        mission_id=None
    ):
        super().__init__(timeout=60)
        self.author_id = author_id
        self.guild_id = guild_id
        self.mission_id = mission_id
        self.choice = None
        self.message = None

    async def interaction_check(self, interaction):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "This mission isn't yours, darling.",
                ephemeral=True
            )
            return False

        return True

    async def finish_mission(self, interaction, choice):
        """Resolve the mission and optionally pay its reward."""
        is_test = self.guild_id is None

        if is_test:
            settings = REVOLUTIONARY_REWARDS[choice]
            success = (
                random.random() < settings["success_chance"]
            )
            pay_range = (
                settings["success_pay"]
                if success
                else settings["failure_pay"]
            )
            reward = random.randint(*pay_range)
        else:
            status, reward, success = complete_mission(
                self.guild_id,
                self.author_id,
                "revolutionary",
                self.mission_id,
                choice
            )

            if status != "success":
                messages = {
                    "expired": "This mission has expired.",
                    "no_mission": "No active mission was found.",
                    "wrong_mission": "This mission is no longer active.",
                    "wrong_job": "Your contract has changed.",
                    "cooldown": "Your next shift isn't available yet.",
                    "invalid_mission": "Invalid mission configuration.",
                }

                await interaction.response.send_message(
                    messages.get(
                        status,
                        "The mission couldn't be completed."
                    ),
                    ephemeral=True
                )
                return

        if choice == "stealth":
            if success:
                result = (
                    "You slipped through the shadows and "
                    "seized the supplies unnoticed."
                )
            else:
                result = (
                    "A guard spotted your movements. "
                    "You escaped with only a few supplies."
                )
        else:
            if success:
                result = (
                    "Your assault overwhelmed the royal guards. "
                    "The convoy is yours."
                )
            else:
                result = (
                    "The guards fought back fiercely. "
                    "Your allies were forced to retreat."
                )

        mission_status = "SUCCESS" if success else "FAILURE"
        strategy = (
            "Stealth" if choice == "stealth" else "Direct Assault"
        )
        livre_emoji = "<:livre:1573206463147544586>"

        reward_label = (
            "Potential reward" if is_test else "Earned"
        )

        closing_message = (
            "*A mere rehearsal. The real battle awaits.*"
            if is_test
            else "*Your next assignment awaits in 30 minutes.*"
        )

        embed = discord.Embed(
            title=(
                f"✦ ───── MISSION {mission_status} ───── ✦"
            ),
            description=(
                "**The Supply Convoy**\n\n"
                f"{result}\n\n"
                f"◈ **Strategy:** {strategy}\n"
                f"{livre_emoji} **{reward_label}:** "
                f"+{reward:,} Livres\n\n"
                f"{closing_message}"
            ),
            color=0x74459A
        )

        embed.set_footer(
            text="THE REAL OLROX • Taking a lot of risks."
        )

        for item in self.children:
            item.disabled = True

        await interaction.response.edit_message(
            embed=embed,
            view=self
        )

        self.choice = choice
        self.stop()

    @discord.ui.button(
        label="Stealth",
        style=discord.ButtonStyle.secondary,
        emoji="🌙"
    )
    async def stealth_button(self, interaction, button):
        await self.finish_mission(interaction, "stealth")

    @discord.ui.button(
        label="Direct Assault",
        style=discord.ButtonStyle.danger,
        emoji="⚔️"
    )
    async def assault_button(self, interaction, button):
        await self.finish_mission(interaction, "assault")

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True

        if self.message is not None:
            try:
                await self.message.edit(view=self)
            except discord.HTTPException:
                pass


class Missions(commands.Cog):
    """Interactive story missions for standard professions."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="missiontest")
    @commands.guild_only()
    async def missiontest(self, ctx):
        """Preview the Revolutionary mission without changing balances."""
        embed = discord.Embed(
            title="✦ ───── REVOLUTIONARY MISSION ───── ✦",
            description=(
                "**The Supply Convoy**\n\n"
                "A royal convoy is transporting supplies "
                "through the countryside.\n"
                "Your allies desperately need those resources.\n\n"
                "**How will you approach the convoy?**\n\n"
                "*Choose your strategy carefully.*"
            ),
            color=0x74459A
        )

        embed.set_footer(
            text="THE REAL OLROX • Taking a lot of risks.",
            icon_url=self.bot.user.display_avatar.url
        )
        view = MissionView(ctx.author.id)
        view.message = await ctx.send(embed=embed, view=view)


async def setup(bot):
    """Register the missions Cog."""
    await bot.add_cog(Missions(bot))
