
import asyncio
import os
import tempfile

import discord
from discord.ext import commands

from commands.voice import create_voice
from models.model import get_class


class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def checking(self, ctx):
        if not ctx.message.attachments:
            embed = discord.Embed(
                title="─── NO EVIDENCE ───",
                description=(
                    "You expect me to analyze thin air?\n\n"
                    "*Send an image, mortal.*"
                ),
                color=0x74459A
            )
            embed.set_footer(
                text="THE REAL OLROX • Eternally unimpressed"
            )
            await ctx.send(embed=embed)
            return

        for attachment in ctx.message.attachments:
            with tempfile.TemporaryDirectory() as temp_dir:
                image_path = os.path.join(
                    temp_dir, "input_image"
                )

                await attachment.save(image_path)

                try:
                    zone, probability, confidence = (
                        await asyncio.to_thread(
                            get_class,
                            model_path="models/keras_model.places.h5",
                            labels="models/labels.places.txt",
                            image_path=image_path
                        )
                    )
                except Exception as error:
                    print("Image classification error:", error)

                    embed = discord.Embed(
                        title="─── ANALYSIS FAILED ───",
                        description=(
                            "This image refuses to reveal its secrets.\n\n"
                            "*How irritating.*"
                        ),
                        color=0x74459A
                    )
                    await ctx.send(embed=embed)
                    continue

                probability = round(probability * 100, 2)

                if zone == "RESTRICTED":
                    title = "─── RESTRICTED AREA ───"
                    message = "WARNING! RESTRICTED AREA!"
                    verdict = (
                        "You have entered forbidden territory.\n\n"
                        "*I suggest you reconsider your choices.*"
                    )
                else:
                    title = "─── ACCESS GRANTED ───"
                    message = (
                        "No problem detected. "
                        "This area is not restricted."
                    )
                    verdict = (
                        "No restrictions detected.\n\n"
                        "*How terribly ordinary.*"
                    )

                embed = discord.Embed(
                    title=title,
                    description=(
                        f"**Zone:** {zone}\n"
                        f"**Probability:** {probability}%\n"
                        f"**Confidence:** {confidence}\n\n"
                        f"{verdict}"
                    ),
                    color=0x74459A
                )

                embed.set_footer(
                    text="THE REAL OLROX • Eternally unimpressed"
                )

                await ctx.send(embed=embed)

                audio_path = os.path.join(
                    temp_dir, "warning.wav"
                )

                try:
                    await asyncio.to_thread(
                        create_voice,
                        message,
                        audio_path
                    )

                    await ctx.send(
                        file=discord.File(
                            audio_path,
                            filename="warning.wav"
                        )
                    )

                except Exception as error:
                    print("Voice error:", error)

                    embed = discord.Embed(
                        title="─── AN UNFORTUNATE SILENCE ───",
                        description=(
                            "My voice is broken, mortal.\n\n"
                            "*Try again later.*"
                        ),
                        color=0x74459A
                    )

                    await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Images(bot))
