# 🦇 The Real Olrox — Discord Bot

*A sarcastic vampire with a suspicious amount of Python knowledge.*

A Python Discord bot inspired by **Olrox from Castlevania: Nocturne**, combining machine learning, English practice, speech recognition, text-to-speech, weather information, and a rather dramatic vampire personality.

Originally developed as a Python learning exercise, the project has evolved from one chaotic script into a modular Discord bot using **Cogs**.

Nothing serious. Just a vampire learning software engineering. xd

## Features

| Command | Description |
|---|---|
| `$hello` | Welcomes mortals with a sarcastic message and an animated GIF |
| `$heh` | Repeats "he" a specified number of times |
| `$fact` | Shares a fact |
| `$say` | Converts text into a WAV audio attachment |
| `$checking` | Classifies images using a trained machine learning model |
| `$english` | Starts an interactive English pronunciation game |
| `$weather` | Displays current weather information |
| `$night` | Displays moon phase, sunrise, and sunset information |
| `$history` | Shares historical information |

## 🗣️ English Learning Game

The `$english` command allows users to practice pronunciation by sending recorded audio messages.

| Option | Level | Activity | Points per answer |
|---|---|---|---|
| 1 | Words | Repeat English words | 10 |
| 2 | Sentences | Repeat short sentences | 20 |
| 3 | Translate | Translate Spanish into English | 30 |
| 4 | Challenge | Repeat longer English sentences | 40 |
| 5 | Play All | Complete all four levels | Up to 300 total |

Each level contains three randomly selected questions.

The game uses Google Speech Recognition to transcribe recordings and compares the recognized text with the expected answers.

Custom GIFs accompany the game, because Olrox apparently cannot teach English without being dramatic.

## 🧠 Machine Learning

The `$checking` command uses a model trained with **Google Teachable Machine** and Keras.

The bot processes uploaded images and predicts one of two classes:

- `RESTRICTED`
- `NOT RESTRICTED`

It displays the predicted class, confidence score, and confidence description, and can generate an audio response.

**Disclaimer:** This is an experimental educational model, not a real security system.

## 🌦️ Weather and Moon Phases

The `$weather` and `$night` commands retrieve information from `wttr.in`.

Weather reports include temperature, weather conditions, custom thumbnails, and sarcastic commentary.

Night reports include the moon phase, sunrise, and sunset.

Custom PNG icons represent weather conditions and the eight principal moon phases.

Because even immortal vampires need to know when the sun is coming up.

## 🔊 Audio Features

The bot uses:

- **pyttsx3** for text-to-speech
- **SpeechRecognition** for speech-to-text
- **pydub** for audio conversion
- **FFmpeg** for processing audio formats
- **asyncio** for asynchronous execution

The bot generates audio attachments rather than joining Discord voice channels.

## 🏰 Project Structure

```text
The-Real-Olrox/
│
├── main.py
├── config.py
├── README.md
├── .gitignore
│
├── commands/
│   ├── __init__.py
│   ├── general.py
│   ├── history.py
│   ├── voice.py
│   ├── weather.py
│   ├── images.py
│   └── english.py
│
├── models/
│   ├── __init__.py
│   ├── model.py
│   ├── keras_model.places.h5
│   └── labels.places.txt
│
└── assets/
    ├── gifs/
    │   ├── olrox.gif
    │   ├── nice.gif
    │   ├── turning.gif
    │   ├── side_eye.gif
    │   ├── shine.gif
    │   └── still.gif
    │
    └── icons/
        ├── sunny.png
        ├── rain.png
        ├── new_moon.png
        └── ...
```

**Note:** `config.py` is used locally and should not be uploaded if it contains private configuration or credentials.

### Modular Architecture

The bot uses the `discord.py` Cogs system to organize its commands into separate modules.

| Module | Responsibility |
|---|---|
| `main.py` | Bot initialization and extension loading |
| `general.py` | Greetings, laughter, and facts |
| `history.py` | Historical information |
| `voice.py` | Text-to-speech generation |
| `weather.py` | Weather and astronomical information |
| `images.py` | Machine learning image classification |
| `english.py` | English learning game and speech recognition |
| `models/model.py` | Image preprocessing and model inference |

This architecture makes the project easier to maintain, debug, and expand.

And prevents `main.py` from becoming a 900-year-old monster again.

## 🛠️ Technologies

- Python 3.11
- discord.py
- TensorFlow / Keras
- Google Teachable Machine
- NumPy
- Pillow
- SpeechRecognition
- pydub
- FFmpeg
- pyttsx3
- Requests
- wttr.in

## ⚙️ Installation

Clone or download the repository.

Install the required Python packages:

```bash
pip install discord.py tensorflow pillow numpy SpeechRecognition pydub pyttsx3 requests
```

Install FFmpeg separately and ensure it is available on your system's PATH.

The machine learning feature requires the trained `.h5` model and its corresponding labels file.

### Discord Configuration

1. Create a bot in the Discord Developer Portal.
2. Enable the Message Content Intent.
3. Invite the bot to a Discord server with the necessary permissions.
4. Configure the `DISCORD_TOKEN` environment variable.
5. Verify that the required models and assets are present.
6. Run:

```bash
python main.py
```

**Security:** Never publish Discord bot tokens, passwords, or private API credentials.

## 🎨 Visual Identity

The bot uses customized Discord embeds featuring:

- Purple accent color (`#74459A`)
- Animated Olrox GIFs
- Weather and moon-phase icons
- Decorative separators
- Sarcastic messages and dramatic responses

The visual identity is inspired by Olrox from *Castlevania: Nocturne*.

## 📚 Learning Objectives

This project explores:

- Python functions, loops, conditionals, and dictionaries
- Object-oriented programming and Discord Cogs
- Asynchronous programming with `asyncio`
- External APIs and HTTP requests
- Machine learning inference
- Image processing
- Speech recognition and synthesis
- Audio conversion
- File and directory management
- Error handling
- Code organization and PEP 8 conventions
- GitHub project documentation

## ⚠️ Limitations

- Weather information depends on `wttr.in`.
- Speech recognition accuracy varies with audio quality.
- Text-to-speech creates audio files, not live voice-channel audio.
- Image classification predictions may be inaccurate.
- Some features require external software or services.
- The bot requires a valid Discord token to run.

---

### 🦇 Final Words

What started as a simple Python exercise became a Discord bot with machine learning, audio processing, custom graphics, interactive games, and modular architecture.

There were errors. There were exceptions. There were questionable decisions.

But the vampire survived.

*Constantly fighting for the 1st place.*

**The Real Olrox — because apparently learning Python wasn't dramatic enough.**
