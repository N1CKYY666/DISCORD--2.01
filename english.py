import asyncio
import os
import random
import string
import tempfile

import discord
import speech_recognition as sr
from discord.ext import commands
from pydub import AudioSegment

recognizer = sr.Recognizer()


def normalize_answer(text):
    """Normalize text before comparing spoken answers."""

    text = text.lower().strip()

    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    text = " ".join(text.split())

    return text


async def transcribe_attachment(attachment):
    """Download, convert and transcribe an audio attachment."""

    suffix = os.path.splitext(attachment.filename)[1] or ".ogg"

    with tempfile.TemporaryDirectory() as temp_dir:
        original_path = os.path.join(
            temp_dir, "input" + suffix
        )
        wav_path = os.path.join(temp_dir, "output.wav")

        await attachment.save(original_path)

        def transcribe():
            audio_segment = AudioSegment.from_file(original_path)
            audio_segment.export(wav_path, format="wav")

            with sr.AudioFile(wav_path) as source:
                audio = recognizer.record(source)

            try:
                text = recognizer.recognize_google(
                    audio,
                    language="en-US"
                )
                return text.lower().strip()

            except sr.UnknownValueError:
                return ""

            except sr.RequestError:
                return None

        return await asyncio.to_thread(transcribe)


class English(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_audio_answer(self, ctx):
        """Wait for the student's audio answer."""

        def check(message):
            return (
                message.author == ctx.author
                and message.channel == ctx.channel
                and len(message.attachments) > 0
            )

        await ctx.send(
            "🎧 Send a voice message or audio file "
            "with your answer."
        )

        try:
            message = await self.bot.wait_for(
                "message",
                timeout=45.0,
                check=check
            )

        except TimeoutError:
            await ctx.send(
                "⌛ Time's up. Start again with `$english`."
            )
            return None

        try:
            answer = await transcribe_attachment(
                message.attachments[0]
            )

        except Exception as error:
            print("Audio processing error:", error)
            await ctx.send(
                "⚠️ I couldn't process that audio, mortal."
            )
            return None

        if answer is None:
            await ctx.send(
                "⚠️ Speech recognition service error."
            )
            return None

        if answer == "":
            await ctx.send(
                "😵‍💫 Bro... was that even English?"
            )

        else:
            await ctx.send(
                f"You said: **{answer}**"
            )

        return answer

    async def level_1(self, ctx):
        words = [
            "apple",
            "house",
            "coffee",
            "teacher",
            "chicken"
        ]

        random.shuffle(words)
        score = 0

        for word in words[:3]:
            await ctx.send(
                f"Repeat this word, mortal:\n**>> {word}**"
            )

            answer = await self.get_audio_answer(ctx)

            if answer is None:
                return score

            if answer == word:
                score += 10

                embed = discord.Embed(
                    title="─── WELL DONE, MORTAL ───",
                    description=(
                        f"**Correct answer:** {word}\n"
                        "**+10 points**\n\n"
                        "*Perhaps you're not entirely hopeless.*"
                    ),
                    color=0x74459A
                )

                image = discord.File(
                    "assets/gifs/nice.gif",
                    filename="nice.gif"
                )

                embed.set_image(
                    url="attachment://nice.gif"
                )

            else:
                embed = discord.Embed(
                    title="─── HOW DISAPPOINTING ───",
                    description=(
                        f"**Correct answer:** {word}\n"
                        "**+0 points**\n\n"
                        "*Was that supposed to be English?*"
                    ),
                    color=0x74459A
                )

                image = discord.File(
                    "assets/gifs/side_eye.gif",
                    filename="side_eye.gif"
                )

                embed.set_image(
                    url="attachment://side_eye.gif"
                )

            embed.set_footer(
                text="THE REAL OLROX • English Lessons"
            )

            await ctx.send(
                embed=embed,
                file=image
            )

        await ctx.send(
            f"🏆 Your Level 1 score: **{score}/30**"
        )

        return score

    async def level_2(self, ctx):
        sentences = [
            "good morning",
            "I like coffee",
            "I have a dog",
            "I am a student"
        ]

        random.shuffle(sentences)
        score = 0

        for sentence in sentences[:3]:
            await ctx.send(
                f"Repeat this sentence, mortal:\n"
                f"**>> {sentence}**"
            )

            answer = await self.get_audio_answer(ctx)

            if answer is None:
                return score

            if answer == sentence.lower():
                score += 20

                embed = discord.Embed(
                    title="─── IMPRESSIVE, MORTAL ───",
                    description=(
                        f"**Correct answer:** {sentence}\n"
                        "**+20 points**\n\n"
                        "*Perhaps there is hope for you after all.*"
                    ),
                    color=0x74459A
                )

                image_name = "nice.gif"

            else:
                embed = discord.Embed(
                    title="─── WHAT WAS THAT? ───",
                    description=(
                        f"**Correct answer:** {sentence}\n"
                        "**+0 points**\n\n"
                        "*I have heard better English from a corpse.*"
                    ),
                    color=0x74459A
                )

                image_name = "side_eye.gif"

            image = discord.File(
                f"assets/gifs/{image_name}",
                filename=image_name
            )

            embed.set_image(
                url=f"attachment://{image_name}"
            )

            embed.set_footer(
                text="THE REAL OLROX • English Lessons"
            )

            await ctx.send(
                embed=embed,
                file=image
            )

        await ctx.send(
            f"🏆 Your Level 2 score: **{score}/60**"
        )

        return score

    async def level_3(self, ctx):
        words = {
            "casa": "house",
            "perro": "dog",
            "gato": "cat",
            "agua": "water",
            "escuela": "school"
        }

        questions = list(words.items())
        random.shuffle(questions)
        score = 0

        for spanish, english in questions[:3]:
            await ctx.send(
                f"Translate this word into English, mortal:\n"
                f"**>> {spanish}**"
            )

            answer = await self.get_audio_answer(ctx)

            if answer is None:
                return score

            if answer == english:
                score += 30

                embed = discord.Embed(
                    title="─── EXCELLENT TRANSLATION ───",
                    description=(
                        f"**Spanish:** {spanish}\n"
                        f"**English:** {english}\n"
                        "**+30 points**\n\n"
                        "*Perhaps your education wasn't entirely wasted.*"
                    ),
                    color=0x74459A
                )

                image_name = "nice.gif"

            else:
                embed = discord.Embed(
                    title="─── HOW EMBARRASSING ───",
                    description=(
                        f"**Spanish:** {spanish}\n"
                        f"**Correct translation:** {english}\n"
                        "**+0 points**\n\n"
                        "*Even centuries of patience have limits.*"
                    ),
                    color=0x74459A
                )

                image_name = "side_eye.gif"

            image = discord.File(
                f"assets/gifs/{image_name}",
                filename=image_name
            )

            embed.set_image(
                url=f"attachment://{image_name}"
            )

            embed.set_footer(
                text="THE REAL OLROX • English Lessons"
            )

            await ctx.send(
                embed=embed,
                file=image
            )

        await ctx.send(
            f"🏆 Your Level 3 score: **{score}/90**"
        )

        return score

    async def level_4(self, ctx):
        sentences = [
            "I usually wake up early",
            "The weather is beautiful today",
            "I would like a cup of coffee",
            "My favorite subject is English",
            "I am learning how to speak English"
        ]

        random.shuffle(sentences)
        score = 0

        for sentence in sentences[:3]:
            await ctx.send(
                "─── THE FINAL CHALLENGE ───\n"
                "Repeat this sentence, mortal:\n"
                f"**>> {sentence}**"
            )

            answer = await self.get_audio_answer(ctx)

            if answer is None:
                return score

            if answer == sentence.lower():
                score += 40

                embed = discord.Embed(
                    title="─── MOST IMPRESSIVE ───",
                    description=(
                        f"**Correct answer:** {sentence}\n"
                        "**+40 points**\n\n"
                        "*Well, well... perhaps you are "
                        "worth teaching after all.*"
                    ),
                    color=0x74459A
                )

                image_name = "nice.gif"

            else:
                embed = discord.Embed(
                    title="─── UTTERLY DISAPPOINTING ───",
                    description=(
                        f"**Correct answer:** {sentence}\n"
                        "**+0 points**\n\n"
                        "*I have lived for centuries, "
                        "and somehow that was still painful.*"
                    ),
                    color=0x74459A
                )

                image_name = "side_eye.gif"

            image = discord.File(
                f"assets/gifs/{image_name}",
                filename=image_name
            )

            embed.set_image(
                url=f"attachment://{image_name}"
            )

            embed.set_footer(
                text="THE REAL OLROX • Final Challenge"
            )

            await ctx.send(
                embed=embed,
                file=image
            )

        await ctx.send(
            f"🏆 Your Level 4 score: **{score}/120**"
        )

        return score

    @commands.command()
    async def english(self, ctx):
        embed = discord.Embed(
            title="─── THE ENGLISH TRIAL ───",
            description=(
                "Welcome to my English lessons, mortal.\n\n"
                "**Choose your challenge:**\n\n"
                "🔤 **1. Words** — 30 points\n"
                "📖 **2. Sentences** — 60 points\n"
                "🌍 **3. Translate** — 90 points\n"
                "🔥 **4. Final Challenge** — 120 points\n"
                "🏆 **5. Play All** — 300 points\n\n"
                "Type **1, 2, 3, 4 or 5**.\n\n"
                "*Try not to disappoint me.*"
            ),
            color=0x74459A
        )

        image = discord.File(
            "assets/gifs/olrox.gif",
            filename="olrox.gif"
        )

        embed.set_image(
            url="attachment://olrox.gif"
        )

        embed.set_footer(
            text="THE REAL OLROX • English Academy"
        )

        await ctx.send(embed=embed, file=image)

        def check(message):
            return (
                message.author == ctx.author
                and message.channel == ctx.channel
                and message.content in ["1", "2", "3", "4", "5"]
            )

        try:
            message = await self.bot.wait_for(
                "message",
                timeout=30.0,
                check=check
            )

        except TimeoutError:
            await ctx.send(
                "⌛ Too slow, mortal. Try `$english` again."
            )
            return

        option = message.content
        total = 0

        levels = {
            "1": self.level_1,
            "2": self.level_2,
            "3": self.level_3,
            "4": self.level_4
        }

        if option == "5":
            selected_levels = list(levels.values())
            maximum = 300
        else:
            selected_levels = [levels[option]]
            maximum = {
                "1": 30,
                "2": 60,
                "3": 90,
                "4": 120
            }[option]

        for level in selected_levels:
            transition = discord.Embed(
                title="─── A NEW CHALLENGE ───",
                description=(
                    "Another trial awaits you.\n\n"
                    "*Do try to keep up.*"
                ),
                color=0x74459A
            )

            image = discord.File(
                "assets/gifs/turning.gif",
                filename="turning.gif"
            )

            transition.set_image(
                url="attachment://turning.gif"
            )

            await ctx.send(
                embed=transition,
                file=image
            )

            total += await level(ctx)

        result = discord.Embed(
            title="─── THE FINAL VERDICT ───",
            description=(
                f"🏆 **Your final score: {total}/{maximum}**\n\n"
                "*Perhaps we shall meet again, mortal.*"
            ),
            color=0x74459A
        )

        result.set_footer(
            text="THE REAL OLROX • English Academy"
        )

        await ctx.send(embed=result)


async def setup(bot):
    await bot.add_cog(English(bot))
