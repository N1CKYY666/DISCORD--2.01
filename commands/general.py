import asyncio
import random

import discord
import requests
from discord.ext import commands


def get_history():
    url = "https://byabbe.se/on-this-day/10/30/events.json"

    response = requests.get(url, timeout=15)

    if response.status_code == 200:
        data = response.json()
        events = data["events"]

        if not events:
            return None

        event = random.choice(events)
        return event["year"], event["description"]

    return None


class History(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def history(self, ctx):
        try:
            result = await asyncio.to_thread(get_history)
        except (requests.RequestException, ValueError, KeyError):
            await ctx.send(
                "The archives are unavailable, mortal."
            )
            return

        if result is None:
            await ctx.send(
                "The archives are unavailable, mortal."
            )
            return

        year, description = result

        embed = discord.Embed(
            title="✦ ───── HISTORY ───── ✦",
            description=(
                f"**Year: {year}**\n\n"
                f"{description}\n\n"
                "*Even eternity cannot erase the past.*"
            ),
            color=0x74459A
        )

        image = discord.File(
            "assets/gifs/snake.gif",
            filename="snake.gif"
        )

        divider = discord.File(
            "assets/gifs/divider1.gif",
            filename="divider1.gif"
        )

        embed.set_thumbnail(
            url="attachment://snake.gif"
        )

        embed.set_image(
            url="attachment://divider1.gif"
        )

        embed.set_footer(
            text="THE REAL OLROX • Richter's childhood nightmare.",
            icon_url=self.bot.user.display_avatar.url
        )

        await ctx.send(embed=embed, files=[image, divider])


async def setup(bot):
    await bot.add_cog(History(bot))
