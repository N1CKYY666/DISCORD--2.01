"""Shared mission interaction views."""

import random
import sqlite3
import time

import discord

from commands.elite_missions import MISSIONS, reward_details
from commands.jobs import DB_PATH
from commands.mission_engine import complete_mission
from commands.mission_styles import (
    decorate_mission_embed,
    get_mission_files,
    mission_color,
)


class MissionView(discord.ui.View):
    """Interactive mission with two possible strategies LMAOOO."""

    def __init__(
        self,
        author_id,
        guild_id=None,
        mission_id="supply_convoy",
        aura_gif=None,
        reservation_token=None
    ):
        super().__init__(timeout=60)
        self.author_id = author_id
        self.guild_id = guild_id
        self.mission_id = mission_id
        self.aura_gif = aura_gif
        self.reservation_token = reservation_token
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
                choice,
                self.reservation_token
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
        _, currency, reward_emoji = reward_details(mission["job"])

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
                f"{reward_emoji} **{reward_label}:** "
                f"+{reward:,} {currency}\n\n"
                f"{closing_message}"
            ),
            color=mission_color(mission["job"])
        )

        embed.set_footer(
            text=(
                "THE REAL OLROX • "
                "Richter's childhood nightmare."
            ),
            icon_url=interaction.client.user.display_avatar.url
        )

        decorate_mission_embed(embed, self.aura_gif, mission["job"])

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
        aura_gif,
        reservation_token
    ):
        super().__init__(timeout=60)

        self.author_id = author_id
        self.guild_id = guild_id
        self.mission_id = mission_id
        self.aura_gif = aura_gif
        self.reservation_token = reservation_token
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

        now = int(time.time())
        new_expiry = max(now + 60, self.reservation_token + 1)
        with sqlite3.connect(DB_PATH, timeout=10) as connection:
            cursor = connection.execute(
                "UPDATE active_missions SET expires_at = ? "
                "WHERE guild_id = ? AND user_id = ? AND job_id = ? "
                "AND mission_id = ? AND expires_at = ? AND expires_at > ?",
                (
                    new_expiry,
                    self.guild_id,
                    self.author_id,
                    job_id,
                    self.mission_id,
                    self.reservation_token,
                    now
                )
            )
            updated = cursor.rowcount
        if not updated:
            await interaction.followup.send(
                "This assignment has expired. Use `$mission` again.",
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
            color=mission_color(mission["job"])
        )

        embed.set_footer(
            text=(
                "THE REAL OLROX • "
                "Richter's childhood nightmare."
            ),
            icon_url=interaction.client.user.display_avatar.url
        )

        decorate_mission_embed(embed, self.aura_gif, mission["job"])

        view = MissionView(
            self.author_id,
            guild_id=self.guild_id,
            mission_id=self.mission_id,
            aura_gif=self.aura_gif,
            reservation_token=new_expiry
        )

        view.message = await interaction.followup.send(
            embed=embed,
            view=view,
            files=get_mission_files(self.aura_gif, job_id),
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
