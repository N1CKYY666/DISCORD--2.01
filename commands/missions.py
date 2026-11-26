"""Mission commands for interactive and elite professions."""

import random
import sqlite3

import discord
from discord.ext import commands

from commands.elite_missions import MISSIONS
from commands.jobs import DB_PATH, JOBS
from commands.mission_engine import get_compatible_items, reserve_mission
from commands.mission_styles import (
    choose_gif,
    decorate_mission_embed,
    get_mission_files,
    mission_color,
)
from commands.mission_views import EquipmentView, MissionView


class Missions(commands.Cog):
    """Interactive story missions for standard professions."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mission")
    @commands.guild_only()
    async def mission(self, ctx):
        """Assign a random mission for the active profession."""
        with sqlite3.connect(DB_PATH) as connection:
            current = connection.execute(
                "SELECT job_id FROM user_jobs "
                "WHERE guild_id = ? AND user_id = ?",
                (ctx.guild.id, ctx.author.id)
            ).fetchone()
        job_id = current[0] if current else None
        job = JOBS.get(job_id)
        if job is None:
            await ctx.send(
                "Choose a profession with `$jobs` and `$job` first."
            )
            return
        if job["mission_type"] == "standard":
            await ctx.send("Your profession uses `$work`, not `$mission`.")
            return
        candidates = [
            key
            for key, data in MISSIONS.items()
            if data["job"] == job_id
        ]
        if not candidates:
            await ctx.send("No assignments are currently available.")
            return
        mission_id = random.choice(candidates)
        mission = MISSIONS[mission_id]
        status, remaining = reserve_mission(
            ctx.guild.id, ctx.author.id, job_id, mission_id
        )
        if status != "reserved":
            messages = {
                "cooldown": (
                    f"Next assignment in {remaining // 60}m "
                    f"{remaining % 60}s."
                ),
                "active_mission": (
                    f"You already have an assignment. "
                    f"{remaining}s remaining."
                ),
                "level": f"This assignment requires level {mission['level']}.",
            }
            await ctx.send(
                messages.get(status, "Your contract is no longer valid.")
            )
            return

        compatible_items = get_compatible_items(
            ctx.guild.id,
            ctx.author.id,
            job_id
        )

        print(
            f"[MISSION EQUIPMENT] "
            f"User: {ctx.author.id} | "
            f"Job: {job_id} | "
            f"Items: {[item[0] for item in compatible_items]}"
        )

        aura_gif = choose_gif(mission["job"])

        equipment_embed = discord.Embed(
            title="✦ ───── MISSION PREPARATION ───── ✦",
            description=(
                f"**{mission['title']}**\n\n"
                "Choose your equipment before beginning.\n\n"
                "You may enter without equipment.\n"
                "*Your choice will be locked once confirmed.*"
            ),
            color=mission_color(mission["job"])
        )
        equipment_embed.set_footer(
            text=(
                "THE REAL OLROX • "
                "Richter's childhood nightmare."
            ),
            icon_url=self.bot.user.display_avatar.url
        )

        equipment_view = EquipmentView(
            ctx.author.id,
            compatible_items,
            ctx.guild.id,
            mission_id,
            aura_gif,
            remaining
        )

        decorate_mission_embed(equipment_embed, aura_gif, job_id)

        equipment_view.message = await ctx.send(
            embed=equipment_embed,
            view=equipment_view,
            files=get_mission_files(aura_gif, mission["job"])
        )

    @commands.command(name="missiontest", hidden=True)
    @commands.is_owner()
    @commands.guild_only()
    async def missiontest(self, ctx, mission_id="supply_convoy"):
        """Preview the Revolutionary mission without changing balances."""
        mission_id = mission_id.lower()

        mission = MISSIONS.get(mission_id)

        if mission is None:
            await ctx.send(
                "That mission does not exist, monsieur."
            )
            return

        embed = discord.Embed(
            title="✦ ───── YOUR MISSION ───── ✦",
            description=(
                f"☾ **{mission['title']}**\n\n"
                f"{mission['description']}\n\n"
                f"☾ **{mission['question']}**\n\n"
                "*Choose your strategy carefully.*"
            ),
            color=mission_color(mission["job"])
        )

        embed.set_footer(
            text=(
                "THE REAL OLROX • "
                "Richter's childhood nightmare."
            ),
            icon_url=self.bot.user.display_avatar.url
        )

        aura_gif = choose_gif(mission["job"])
        decorate_mission_embed(embed, aura_gif, mission["job"])

        view = MissionView(
            ctx.author.id,
            mission_id=mission_id,
            aura_gif=aura_gif
        )
        view.message = await ctx.send(
            embed=embed,
            view=view,
            files=get_mission_files(aura_gif, mission["job"])
        )


async def setup(bot):
    """Register the missions Cog."""
    await bot.add_cog(Missions(bot))
