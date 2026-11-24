import asyncio
import os

import discord
from discord.ext import commands

# Configure the Discord intents required by the bot.
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Create the bot and define its command prefix.
bot = commands.Bot(command_prefix="$", intents=intents)


@bot.event
async def on_ready():
    """Display a confirmation when the bot connects to Discord."""
    print(f"We have logged in as {bot.user}")


async def main():
    """Load the bot extensions and establish the Discord connection."""
    async with bot:
        # Load the command modules (Cogs).
        await bot.load_extension("commands.general")
        await bot.load_extension("commands.history")
        await bot.load_extension("commands.voice")
        await bot.load_extension("commands.weather")
        # await bot.load_extension("commands.images") JUEPUTA NO SIRVE
        await bot.load_extension("commands.english")
        await bot.load_extension("commands.social")
        await bot.load_extension("commands.levels")
        await bot.load_extension("commands.economy")
        await bot.load_extension("commands.jobs")
        await bot.load_extension("commands.work")
        await bot.load_extension("commands.missions")
        await bot.load_extension("commands.shop")
        await bot.load_extension("commands.gift")

        # Connect to Discord using the environment token.
        await bot.start(os.environ["DISCORD_TOKEN"])


# Run the bot only when this file is executed directly.
if __name__ == "__main__":
    asyncio.run(main())
