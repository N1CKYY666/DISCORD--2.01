import asyncio
import os
import tempfile

import discord
import pyttsx3
from discord.ext import commands


def create_voice(text, file_path):
    engine = pyttsx3.init()

    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    engine.setProperty("rate", 150)
    engine.setProperty("volume", 1)

    engine.save_to_file(text, file_path)
    engine.runAndWait()
    engine.stop()


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *, text):
        if len(text) > 200:
            embed = discord.Embed(
                title="─── A LITTLE RESTRAINT ───",
                description=(
                    "Two hundred characters, mortal.\n\n"
                    "*Even my patience has its limits.*"
                ),
                color=0x74459A
            )

            embed.set_footer(
                text="THE REAL OLROX • Eternally unimpressed"
            )

            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title="─── THE VOICE OF ETERNITY ───",
            description=(
                "**You wish to hear my voice?**\n\n"
                f"*\"{text}\"*\n\n"
                "How terribly demanding."
            ),
            color=0x74459A
        )

        image = discord.File(
            "assets/gifs/olrox.gif",
            filename="olrox.gif"
        )

        embed.set_thumbnail(
            url="attachment://olrox.gif"
        )

        embed.set_footer(
            text="THE REAL OLROX • Eternally unimpressed"
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            audio_path = os.path.join(
                temp_dir, "robot.wav"
            )

            try:
                await asyncio.to_thread(
                    create_voice, text, audio_path
                )

                await ctx.send(
                    embed=embed,
                    files=[
                        image,
                        discord.File(
                            audio_path,
                            filename="robot.wav"
                        )
                    ]
                )

            except Exception as error:
                print("Voice error:", error)

                error_embed = discord.Embed(
                    title="─── AN UNFORTUNATE SILENCE ───",
                    description=(
                        "My voice seems to have failed me.\n\n"
                        "*How inconvenient.*"
                    ),
                    color=0x74459A
                )

                await ctx.send(embed=error_embed)


async def setup(bot):
    await bot.add_cog(Voice(bot))
