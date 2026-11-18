import asyncio
import os
import tempfile

import discord
import pyttsx3
from discord.ext import commands

FOOTER_TEXT = "THE REAL OLROX • Richter's childhood nightmare."


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

    async def send_styled_embed(self, ctx, embed, extra_files=None):
        """Apply the Olrox thumbnail, divider and footer consistently."""
        image = discord.File(
            "assets/gifs/olrox.gif",
            filename="olrox.gif"
        )
        divider = discord.File(
            "assets/gifs/divider1.gif",
            filename="divider1.gif"
        )

        embed.set_thumbnail(url="attachment://olrox.gif")
        embed.set_image(url="attachment://divider1.gif")
        embed.set_footer(
            text=FOOTER_TEXT,
            icon_url=self.bot.user.display_avatar.url
        )

        files = [image, divider]
        if extra_files:
            files.extend(extra_files)

        await ctx.send(embed=embed, files=files)

    @commands.command()
    async def say(self, ctx, *, text):
        if len(text) > 200:
            embed = discord.Embed(
                title="✦ ───── A LITTLE RESTRAINT ───── ✦",
                description=(
                    "Two hundred characters, mortal.\n\n"
                    "*Even my patience has its limits.*"
                ),
                color=0x74459A
            )
            await self.send_styled_embed(ctx, embed)
            return

        embed = discord.Embed(
            title="✦ ───── THE VOICE OF ETERNITY ───── ✦",
            description=(
                "**You wish to hear my voice?**\n\n"
                f'*"{text}"*\n\n'
                "How terribly demanding."
            ),
            color=0x74459A
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            audio_path = os.path.join(temp_dir, "robot.wav")

            try:
                await asyncio.to_thread(
                    create_voice, text, audio_path
                )

                await self.send_styled_embed(
                    ctx,
                    embed,
                    extra_files=[discord.File(audio_path, filename="robot.wav")]
                )

            except Exception as error:
                print("Voice error:", error)

                error_embed = discord.Embed(
                    title="✦ ───── AN UNFORTUNATE SILENCE ───── ✦",
                    description=(
                        "My voice seems to have failed me.\n\n"
                        "*How inconvenient.*"
                    ),
                    color=0x74459A
                )
                await self.send_styled_embed(ctx, error_embed)


async def setup(bot):
    await bot.add_cog(Voice(bot))
