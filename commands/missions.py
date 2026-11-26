"""Interactive mission interfaces for The Real Olrox."""

import random
import sqlite3
import time
from pathlib import Path

import discord
from discord.ext import commands

from commands.item_effects import ITEM_EFFECTS
from commands.jobs import DB_PATH
from commands.mission_data import MISSIONS
from commands.shop import get_user_inventory
from commands.work import WORK_COOLDOWN

GIF_DIR = Path(__file__).resolve().parent.parent / "assets" / "gifs"

DIVIDER_GIF = GIF_DIR / "divider1.gif"
AURA_GIFS = [
    GIF_DIR / "aura_farming.gif",
    GIF_DIR / "power.gif",
    GIF_DIR / "hair.gif",
    GIF_DIR / "castle.gif",
    GIF_DIR / "richter4.gif",
    GIF_DIR / "trevor.gif",
    GIF_DIR / "richter.gif",
    *GIF_DIR.glob("mizrak*.gif"),
    GIF_DIR / "alucard.gif",
    GIF_DIR / "summon.gif",
    GIF_DIR / "richter3.gif",
    GIF_DIR / "shove.gif",
    *GIF_DIR.glob("sypha*.gif"),
    *GIF_DIR.glob("another*.gif"),
]


def decorate_mission_embed(embed, aura_gif):
    """Apply the standard mission embed appearance."""
    embed.set_thumbnail(url=f"attachment://{aura_gif.name}")
    embed.set_image(url="attachment://divider1.gif")
    return embed


def get_mission_files(aura_gif):
    """Create the GIF attachments for a mission message."""
    return [
        discord.File(DIVIDER_GIF, filename="divider1.gif"),
        discord.File(aura_gif, filename=aura_gif.name)
    ]


def get_compatible_items(guild_id, user_id, job_id):
    """Return owned mission items compatible with a profession."""
    inventory = get_user_inventory(guild_id, user_id)
    compatible_items = []

    for item_id, item_data, quantity in inventory:
        effect = ITEM_EFFECTS.get(item_id)

        if effect is None:
            continue

        allowed_jobs = effect["jobs"]

        if allowed_jobs != "all" and job_id not in allowed_jobs:
            continue

        compatible_items.append(
            (item_id, item_data, quantity, effect)
        )

    return compatible_items


def get_revolutionary_mission():
    """Return the first Revolutionary mission."""
    return MISSIONS["supply_convoy"]


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

    mission = MISSIONS.get(mission_id)

    if (
        mission is None
        or mission["job"] != job_id
        or choice not in mission["choices"]
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

        settings = mission["choices"][choice]
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


REVOLUTIONARY_REWARDS = MISSIONS["supply_convoy"]["choices"]


class MissionView(discord.ui.View):
    """Interactive mission with two possible strategies LMAOOO."""

    def __init__(
        self,
        author_id,
        guild_id=None,
        mission_id="supply_convoy",
        aura_gif=None
    ):
        super().__init__(timeout=60)
        self.author_id = author_id
        self.guild_id = guild_id
        self.mission_id = mission_id
        self.aura_gif = aura_gif
        self.choice = None
        self.message = None
        mission = MISSIONS[self.mission_id]

        for choice_id, choice_data in mission["choices"].items():
            button = discord.ui.Button(
                label=choice_data["label"],
                emoji=choice_data["emoji"],
                style=(
                    discord.ButtonStyle.danger
                    if choice_id == "assault"
                    else discord.ButtonStyle.secondary
                )
            )

            async def callback(interaction, selected=choice_id):
                await self.finish_mission(interaction, selected)

            button.callback = callback
            self.add_item(button)

    async def interaction_check(self, interaction):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "This mission belongs to another player.",
                ephemeral=True
            )
            return False

        return True

    async def finish_mission(self, interaction, choice):
        """Resolve the mission and optionally pay its reward."""
        is_test = self.guild_id is None

        if is_test:
            settings = MISSIONS[self.mission_id]["choices"][choice]
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
                MISSIONS[self.mission_id]["job"],
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

        mission = MISSIONS[self.mission_id]
        choice_data = mission["choices"][choice]

        result = (
            choice_data["success_text"]
            if success
            else choice_data["failure_text"]
        )

        mission_status = "SUCCESS" if success else "FAILURE"
        strategy = choice_data["label"]
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
                f"**{mission['title']}**\n\n"
                f"{result}\n\n"
                f"◈ **Strategy:** {strategy}\n"
                f"{livre_emoji} **{reward_label}:** "
                f"+{reward:,} Livres\n\n"
                f"{closing_message}"
            ),
            color=0x74459A
        )

        embed.set_footer(
            text=(
                "THE REAL OLROX • "
                "Richter's childhood nightmare."
            ),
            icon_url=interaction.client.user.display_avatar.url
        )

        decorate_mission_embed(embed, self.aura_gif)

        for item in self.children:
            item.disabled = True

        await interaction.response.edit_message(
            embed=embed,
            view=self
        )

        self.choice = choice
        self.stop()

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True

        if self.message is not None:
            try:
                await self.message.edit(view=self)
            except discord.HTTPException:
                pass


class EquipmentSelect(discord.ui.Select):
    """Allow a player to choose mission equipment."""

    def __init__(self, compatible_items):
        options = [
            discord.SelectOption(
                label="No Equipment",
                value="none",
                description="Enter the mission without equipment."
            )
        ]

        for item_id, item_data, quantity, effect in compatible_items:
            options.append(
                discord.SelectOption(
                    label=item_data["name"],
                    value=item_id,
                    description=f"Available: {quantity}"
                )
            )

        super().__init__(
            placeholder="Choose your equipment...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction):
        selected_item = self.values[0]

        self.view.selected_item = selected_item

        await interaction.response.send_message(
            f"Selected equipment: **{selected_item}**\n"
            "Press Confirm Equipment to lock your choice.",
            ephemeral=True
        )


class EquipmentView(discord.ui.View):
    """Mission equipment preparation interface."""

    def __init__(
        self,
        author_id,
        compatible_items,
        guild_id,
        mission_id,
        aura_gif
    ):
        super().__init__(timeout=60)

        self.author_id = author_id
        self.guild_id = guild_id
        self.mission_id = mission_id
        self.aura_gif = aura_gif
        self.selected_item = "none"
        self.confirmed = False
        self.message = None

        self.add_item(EquipmentSelect(compatible_items))

    async def interaction_check(self, interaction):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "This equipment belongs to another player.",
                ephemeral=True
            )
            return False

        return True

    @discord.ui.button(
        label="Confirm Equipment",
        style=discord.ButtonStyle.success
    )
    async def confirm_equipment(self, interaction, button):
        if self.confirmed:
            return

        await interaction.response.defer()

        mission = MISSIONS[self.mission_id]
        job_id = mission["job"]

        status, remaining = reserve_mission(
            self.guild_id,
            self.author_id,
            job_id,
            self.mission_id
        )

        if status != "reserved":
            messages = {
                "cooldown": "You must wait before your next mission.",
                "wrong_job": "This mission is not for your profession.",
                "unemployed": "You need a profession first.",
                "active_mission": "You already have an active mission."
            }

            await interaction.followup.send(
                messages.get(
                    status,
                    "This mission is currently unavailable."
                ),
                ephemeral=True
            )
            return

        self.confirmed = True

        for item in self.children:
            item.disabled = True

        await interaction.message.edit(view=self)

        embed = discord.Embed(
            title="✦ ───── MISSION ───── ✦",
            description=(
                f"**{mission['title']}**\n\n"
                f"{mission['description']}\n\n"
                f"**Equipment:** {self.selected_item}\n\n"
                f"**{mission['question']}**\n\n"
                "*Choose your strategy carefully.*"
            ),
            color=0x74459A
        )

        embed.set_footer(
            text=(
                "THE REAL OLROX • "
                "Richter's childhood nightmare."
            ),
            icon_url=interaction.client.user.display_avatar.url
        )

        decorate_mission_embed(embed, self.aura_gif)

        view = MissionView(
            self.author_id,
            guild_id=self.guild_id,
            mission_id=self.mission_id,
            aura_gif=self.aura_gif
        )

        view.message = await interaction.followup.send(
            embed=embed,
            view=view,
            files=get_mission_files(self.aura_gif),
            wait=True
            )

        self.stop()

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

    @commands.command(name="mission")
    @commands.guild_only()
    async def mission(self, ctx, mission_id="supply_convoy"):
        """Start a mission with real rewards."""
        mission_id = mission_id.lower()
        mission = MISSIONS.get(mission_id)

        if mission is None:
            await ctx.send(
                "That mission does not exist, monsieur."
            )
            return

        job_id = mission["job"]

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

        aura_gif = random.choice(AURA_GIFS)

        equipment_embed = discord.Embed(
            title="✦ ───── MISSION PREPARATION ───── ✦",
            description=(
                f"**{mission['title']}**\n\n"
                "Choose your equipment before beginning.\n\n"
                "You may enter without equipment.\n"
                "*Your choice will be locked once confirmed.*"
            ),
            color=0x74459A
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
            aura_gif
        )

        decorate_mission_embed(equipment_embed, aura_gif)

        equipment_view.message = await ctx.send(
            embed=equipment_embed,
            view=equipment_view,
            files=get_mission_files(aura_gif)
        )

    @commands.command(name="missiontest")
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
            color=0x74459A
        )

        embed.set_footer(
            text=(
                "THE REAL OLROX • "
                "Richter's childhood nightmare."
            ),
            icon_url=self.bot.user.display_avatar.url
        )

        aura_gif = random.choice(AURA_GIFS)
        decorate_mission_embed(embed, aura_gif)

        view = MissionView(
            ctx.author.id,
            mission_id=mission_id,
            aura_gif=aura_gif
        )
        view.message = await ctx.send(
            embed=embed,
            view=view,
            files=get_mission_files(aura_gif)
        )


async def setup(bot):
    """Register the missions Cog."""
    await bot.add_cog(Missions(bot))
