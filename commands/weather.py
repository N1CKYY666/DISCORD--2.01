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

    @commands.command()
    async def weather(self, ctx, *, city: str):
        try:
            climate = await asyncio.to_thread(
                get_me_weather, city
            )
        except requests.RequestException:
            climate = None

        if not climate or "|" not in climate:
            embed = discord.Embed(
                title="─── THE SILENT SKIES ───",
                description=(
                    "The skies refuse to answer me, mortal.\n\n"
                    "*How terribly inconvenient.*"
                ),
                color=0x74459A
            )

            await ctx.send(embed=embed)
            return

        condition, temperature = climate.split("|", 1)

        condition = condition.strip()
        temperature = temperature.strip()

        phrases = [
            "Even the weather is more interesting than you.",
            "Centuries of wisdom, wasted on weather reports.",
            "I suppose you needed me to look at the sky for you.",
            "How delightful. Another day among mortals."
        ]

        phrase = random.choice(phrases)

        embed = discord.Embed(
            title="─── THE FORECAST ───",
            description=(
                f"**Location:** {city}\n\n"
                f"**Weather:** {condition}\n"
                f"**Temperature:** {temperature}\n\n"
                f'*"{phrase}"*'
            ),
            color=0x74459A
        )

        embed.set_footer(
            text=(
                "THE REAL OLROX • "
                "Weather Report... Unfortunately."
            )
        )

        image_name = weather_images.get(
            condition.lower()
        )

        message = (
            f"The weather in {city} is "
            f"{condition}, {temperature}"
        )

        spoken_message = message.replace(
            "°C", " degrees Celsius"
        )

        if image_name:
            image_path = os.path.join(
                "assets",
                "icons",
                image_name
            )

            if os.path.isfile(image_path):
                image = discord.File(
                    image_path,
                    filename=image_name
                )

                embed.set_thumbnail(
                    url=f"attachment://{image_name}"
                )

                await ctx.send(embed=embed, file=image)
            else:
                await ctx.send(embed=embed)
        else:
            await ctx.send(embed=embed)

        with tempfile.TemporaryDirectory() as temp_dir:
            audio_path = os.path.join(
                temp_dir, "weather.wav"
            )

            try:
                await asyncio.to_thread(
                    create_voice,
                    spoken_message,
                    audio_path
                )

                await ctx.send(
                    file=discord.File(
                        audio_path,
                        filename="weather.wav"
                    )
                )

            except Exception as error:
                print("Voice error:", error)

                error_embed = discord.Embed(
                    title="─── AN UNFORTUNATE SILENCE ───",
                    description=(
                        "My voice is broken, mortal.\n\n"
                        "*A temporary inconvenience.*"
                    ),
                    color=0x74459A
                )

                await ctx.send(embed=error_embed)

    @commands.command()
    async def night(self, ctx, *, city: str):
        try:
            climate = await asyncio.to_thread(
                get_night_weather, city
            )
        except requests.RequestException:
            climate = None

        if not climate or climate.count("|") != 2:
            embed = discord.Embed(
                title="─── THE SILENT HEAVENS ───",
                description=(
                    "The heavens refuse to answer me, mortal.\n\n"
                    "*How disappointing.*"
                ),
                color=0x74459A
            )

            embed.set_footer(
                text="THE REAL OLROX • Eternally unimpressed"
            )

            await ctx.send(embed=embed)
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
            title="─── NIGHTS FORECAST ───",
            description=(
                f"**Location:** {city}\n\n"
                f"**Moon phase:** {moon}\n"
                f"**Sunrise:** {sunrise}\n"
                f"**Sunset:** {sunset}\n\n"
                f'*"{phrase}"*'
            ),
            color=0x74459A
        )

        embed.set_footer(
            text="THE REAL OLROX • Night Report For You, Dumbass"
        )

        image_name = moon_images.get(moon)

        if image_name:
            image_path = os.path.join(
                "assets",
                "icons",
                image_name
            )

            if os.path.isfile(image_path):
                image = discord.File(
                    image_path,
                    filename=image_name
                )

                embed.set_thumbnail(
                    url=f"attachment://{image_name}"
                )

                await ctx.send(embed=embed, file=image)
                return

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Weather(bot))
