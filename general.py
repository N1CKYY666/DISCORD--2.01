
import asyncio
import random

import discord
import requests
from discord.ext import commands


# Gets a random fact from the API
def get_random_fact():
    url = "https://uselessfacts.jsph.pl/random.json?language=en"

    response = requests.get(url, timeout=15)

    if response.status_code == 200:
        data = response.json()
        return data["text"]
    else:
        return None


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def fact(self, ctx):

        fact_text = await asyncio.to_thread(get_random_fact)

        if fact_text is None:
            await ctx.send(
                "The archives are unavailable. Please try again later."
            )
            return

        phrases = [
            "Try to remember that",
            "Even you might find this interesting.",
            "You're welcome.",
            "How delightful. Another day among mortals."
        ]

        phrase = random.choice(phrases)

        embed = discord.Embed(
            title="─── A CURIOUS DISCOVERY ───",
            description=(
                f"•** Did you know?**\n\n"
                f"{fact_text}\n\n"
                f"───────────────\n\n"
                f'*"{phrase}"*'
            ),
            color=0x74459A
        )

        image = discord.File(
            "shine.gif",
            filename="shine.gif"
        )

        embed.set_thumbnail(
            url="attachment://shine.gif"
        )

        embed.set_footer(
            text="THE REAL OLROX • Richter's childhood nightmare."
        )

        await ctx.send(embed=embed, file=image)

    @commands.command()
    async def hello(self, ctx):
        """Welcome users with an Olrox-themed message and GIF."""
        embed = discord.Embed(
            title="𝌺 AN UNEXPECTED VISITOR",
            description=(
                "**Well, well... Look who decided to show up.**\n\n"
                "Welcome to my domain.\n"
                "Try not to disappoint me."
            ),
            color=0x74459A
        )

        # Attach Olrox's GIF to the welcome message.
        image = discord.File(
            "assets/gifs/olrox.gif",
            filename="olrox.gif"
        )

        embed.set_thumbnail(
            url="attachment://olrox.gif"
        )

        embed.set_footer(
            text="THE REAL OLROX • Lil boy Belmont..."
        )

        await ctx.send(embed=embed, file=image)

    @commands.command()
    async def heh(self, ctx, count_heh=5):
        """Repeat 'he' a specified number of times."""
        await ctx.send("he" * count_heh)


async def setup(bot):
    await bot.add_cog(General(bot))
