import asyncio
import os
import random
import tempfile

import discord
import requests
from discord.ext import commands

from commands.voice import create_voice


def get_me_weather(city: str):
    base_url = f"https://wttr.in/{city}?format=%C|%t"
    response = requests.get(base_url, timeout=15)
    if response.status_code == 200:
        return response.text.strip()
    return None


weather_images = {
    "sunny": "sunny.png",
    "clear": "sunny.png",
    "partly cloudy": "partly_cloudy.png",
    "cloudy": "cloudy.png",
    "overcast": "cloudy.png",
    "rain": "rain.png",
    "light rain": "rain.png",
    "heavy rain": "rain.png",
    "thunderstorm": "thunderstorm.png",
    "snow": "snow.png",
    "windy": "wind.png"
}


def get_night_weather(city: str):
    base_url = f"https://wttr.in/{city}?format=%m|%S|%s"
    response = requests.get(base_url, timeout=15)
    if response.status_code == 200:
        return response.text.strip()
    return None


moon_images = {
    "🌑": "new_moon.png",
    "🌒": "waxing_crescent.png",
    "🌓": "first_quarter.png",
    "🌔": "waxing_gibbous.png",
    "🌕": "full_moon.png",
    "🌖": "waning_gibbous.png",
    "🌗": "last_quarter.png",
    "🌘": "waning_crescent.png"
}


class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_styled_embed(self, ctx, embed, image_name=None):
        """Send an embed with its existing icon and divider2.gif."""
        files = []
        if image_name:
            image_path = os.path.join("assets", "icons", image_name)
            if os.path.isfile(image_path):
                files.append(discord.File(image_path, filename=image_name))
                embed.set_thumbnail(url=f"attachment://{image_name}")

        divider_path = os.path.join("assets", "gifs", "divider2.gif")
        files.append(discord.File(divider_path, filename="divider2.gif"))
        embed.set_image(url="attachment://divider2.gif")
        embed.set_footer(
            text="THE REAL OLROX • Richter's childhood nightmare.",
            icon_url=self.bot.user.display_avatar.url
        )
        await ctx.send(embed=embed, files=files)

    @commands.command()
    async def weather(self, ctx, *, city: str):
        try:
            climate = await asyncio.to_thread(get_me_weather, city)
        except requests.RequestException:
            climate = None

        if not climate or "|" not in climate:
            embed = discord.Embed(
                title="✦ ───── THE SILENT SKIES ───── ✦",
                description=(
                    "The skies refuse to answer me.\n\n"
                    "*How terribly inconvenient.*"
                ),
                color=0x74459A
            )
            await self.send_styled_embed(ctx, embed)
            return

        condition, temperature = climate.split("|", 1)
        condition = condition.strip()
        temperature = temperature.strip()

        phrases = [
            "Even the weather is more interesting than you.",
            "My time, wasted on weather reports.",
            "I suppose you needed me to look at the sky for you.",
            "How delightful."
        ]
        phrase = random.choice(phrases)

        embed = discord.Embed(
            title="✦ ───── THE FORECAST ───── ✦",
            description=(
                f"**Location:** {city}\n\n"
                f"**Weather:** {condition}\n"
                f"**Temperature:** {temperature}\n\n"
                f'*"{phrase}"*'
            ),
            color=0x74459A
        )

        image_name = weather_images.get(condition.lower())
        await self.send_styled_embed(ctx, embed, image_name)

        message = f"The weather in {city} is {condition}, {temperature}"
        spoken_message = message.replace("°C", " degrees Celsius")

        with tempfile.TemporaryDirectory() as temp_dir:
            audio_path = os.path.join(temp_dir, "weather.wav")
            try:
                await asyncio.to_thread(create_voice, spoken_message, audio_path)
                await ctx.send(
                    file=discord.File(audio_path, filename="weather.wav")
                )
            except Exception as error:
                print("Voice error:", error)
                error_embed = discord.Embed(
                    title="✦ ───── AN UNFORTUNATE SILENCE ───── ✦",
                    description=(
                        "My voice is broken.\n\n"
                        "*A temporary inconvenience.*"
                    ),
                    color=0x74459A
                )
                await self.send_styled_embed(ctx, error_embed)

    @commands.command()
    async def night(self, ctx, *, city: str):
        try:
            climate = await asyncio.to_thread(get_night_weather, city)
        except requests.RequestException:
            climate = None

        if not climate or climate.count("|") != 2:
            embed = discord.Embed(
                title="✦ ───── THE SILENT HEAVENS ───── ✦",
                description=(
                    "The heavens refuse to answer me.\n\n"
                    "*How disappointing.*"
                ),
                color=0x74459A
            )
            await self.send_styled_embed(ctx, embed)
            return

        moon, sunrise, sunset = climate.split("|")
        moon = moon.strip()
        sunrise = sunrise.strip()
        sunset = sunset.strip()

        phrases = [
            "The sun is finally leaving. I can visit Mizrak.",
            "Another night, and I'm quite hungry.",
            "The darkness approaches.",
            "I suppose even the heavens have their schedule."
        ]
        phrase = random.choice(phrases)

        embed = discord.Embed(
            title="✦ ───── NIGHTS FORECAST ───── ✦",
            description=(
                f"**Location:** {city}\n\n"
                f"**Moon phase:** {moon}\n"
                f"**Sunrise:** {sunrise}\n"
                f"**Sunset:** {sunset}\n\n"
                f'*"{phrase}"*'
            ),
            color=0x74459A
        )
        image_name = moon_images.get(moon)
        await self.send_styled_embed(ctx, embed, image_name)


async def setup(bot):
    await bot.add_cog(Weather(bot))
