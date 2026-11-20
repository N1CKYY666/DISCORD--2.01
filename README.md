#  The Real Olrox — Discord Bot

*A sarcastic buddy with a suspicious amount of Python knowledge.*

A Python Discord bot inspired by **Olrox from Castlevania: Nocturne**, combining machine learning, English practice, speech recognition, text-to-speech, weather information, historical facts, social interactions, and an SQLite-based experience system. Made by a teenager who's still trying to learn.

Originally developed as a Python learning exercise, the project has evolved from one chaotic script into a modular Discord bot using **Cogs**.

Nothing serious. Just a vampire learning software engineering. xd

## Features

### General Commands

| Command | Description |
|---|---|
| `$hello` | Displays a sarcastic welcome message with an animated GIF |
| `$heh` | Repeats "he" a specified number of times |
| `$fact` | Shares a random fact |
| `$history` | Shares historical information |

### Weather & Audio

| Command | Description |
|---|---|
| `$weather <city>` | Displays current weather conditions and generates an audio report |
| `$night <city>` | Displays moon phase, sunrise, and sunset information |
| `$say <text>` | Converts text into a WAV audio attachment |

### Interactive Features

| Command | Description |
|---|---|
| `$checking` | Classifies images using a trained machine learning model |
| `$english` | Starts an interactive English pronunciation game |

### Social Commands

| Command | Description |
|---|---|
| `$profile` | Displays your Discord server profile |
| `$profile @user` | Displays another member's profile |
| `$server` | Displays information about the Discord server |
| `$testwelcome` | Tests the welcome message (administrator only) |
| `$testgoodbye` | Tests the farewell message (administrator only) |

### Experience & Rankings

| Command | Description |
|---|---|
| `$rank` | Displays your level, total XP, progress bar, and XP needed for the next level |
| `$rank @user` | Displays another member's level and XP progress |
| `$addxp @user <amount>` | Awards XP and synchronizes the member's progression role (administrator only) |
| `$leaderboard` | Displays the top 10 members by experience |
| `$top` | Alias for `$leaderboard` |

### The Economy

The Real Olrox features a server-based virtual economy
inspired by Revolutionary France (Basically, the serie's whole background)

Two currencies are used:

- **Livres:** The standard currency for everyday activities.
- **Louis d'or:** A special currency reserved for future
  achievements, events, and exclusive rewards.

| Command | Description |
|---|---|
| `$balance` | Displays a member's Livres and Louis d'or |
| `$bal` | Alias for `$balance` |
| `$balance @user` | Displays another member's balance |
| `$daily` | Claims 150 Livres once every 24 hours |

Balances and daily cooldowns are stored in SQLite.

The economy uses custom Discord currency emojis and
themed animated embeds.

### Planned Economy Features

- Level-based professions and random jobs
- Shop and inventory
- Gifts and transfers
- Robbery with cooldowns and penalties
- Virtual-currency casino games

These features are planned and not yet implemented, please have faith in me lmao

## 🏆 Experience & Ranking System

The bot includes a persistent experience system powered by **SQLite**.

Members can earn experience points through regular server activity, while administrators can manually reward users.

### Automatic XP

- Regular messages award a random amount between **5 and 15 XP**.
- Each user has a **60-second cooldown** between rewards.
- Bot messages and commands beginning with `$` do not generate XP.
- Experience is stored separately for each Discord server.
- XP remains saved after the bot restarts.

### Levels and Progression

XP accumulates across levels. Each new level requires more total XP than the previous one. The `$rank` command shows the current level, total XP, a ten-segment progress bar, and the XP remaining until the next level.

When a member earns enough XP from regular messages to reach a new level, Olrox posts a **LEVEL UP** embed with the new level, total XP, and themed animated GIFs. The administrator-only `$addxp` command updates XP and roles immediately, but does not currently send a LEVEL UP announcement.

### Automatic Progression Roles

| Required level | Total XP required | Role |
|---|---:|---|
| 5 | 700 | The Speaker |
| 10 | 2,700 | The Forgemaster |
| 20 | 10,450 | The Dhampir |
| 35 | 31,450 | The Noble |
| 50 | 63,700 | The Vampire Messiah |

These thresholds follow the current `calculate_level()` function in `commands/levels.py`. XP and levels continue beyond level 50; level 50 is simply the highest configured progression role.

- Only **one progression role** is kept at a time: the new role replaces the previous progression role.
- Unrelated server roles are left unchanged.
- Roles are synchronized when XP is awarded through eligible messages or `$addxp`.
- The bot requires **Manage Roles** permission, and its own Discord role must be positioned above all progression roles.

### SQLite Database

Experience records are stored in `data/olrox.db`.

The database uses a table containing:

| Field | Purpose |
|---|---|
| `guild_id` | Identifies the Discord server |
| `user_id` | Identifies the server member |
| `xp` | Stores accumulated experience points |

The combination of `guild_id` and `user_id` acts as the primary key.

SQL operations include table creation, inserting experience, updating existing records, retrieving individual XP totals, and generating leaderboards.

**Note:** The local database should not be committed to the public repository.

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

Custom GIFs accompany correct and incorrect answers, transitions, and challenge screens.

**Note:** The game's scores are currently separate from the SQLite server experience system.

Because Olrox apparently cannot teach English without being dramatic.

## 🧠 Machine Learning

The `$checking` command uses a model trained with **Google Teachable Machine** and Keras.

The bot processes uploaded images and predicts one of two classes:

- `RESTRICTED`
- `NOT RESTRICTED`

It displays the predicted class, confidence score, and confidence description, and can generate an audio response.

The machine learning files are organized inside the `models/` directory.

**Disclaimer:** This is an experimental educational model, not a real security system.

## 🌦️ Weather and Moon Phases

The `$weather` and `$night` commands retrieve information from `wttr.in`.

Weather reports include:

- City and weather conditions
- Temperature
- Custom weather thumbnails
- Random sarcastic commentary
- Text-to-speech audio reports

Night reports include:

- Current moon phase
- Sunrise time
- Sunset time
- Custom moon-phase thumbnails

Custom PNG icons represent weather conditions and the eight principal moon phases.

Because even a vampire needs to know when the sun is coming up.

## Social Interactions

The `social.py` Cog handles server events and member information.

### Welcome & Farewell Messages

When a member joins or leaves, the bot can automatically send a customized embed to the corresponding server channel.

- `bienvenidas` — Welcome messages
- `despedidas` — Farewell messages

These messages feature member avatars, decorative GIFs, and Olrox's distinctive personality.

Administrators can test both events without requiring someone to join or leave the server.

### Member Profiles

The `$profile` command displays information such as:

- Display name
- Server join date
- Account creation date
- Server roles
- Discord status
- Bot account identification

The `$server` command provides information about the server, including its name, owner, creation date, member count, and roles.

## Audio Features

The bot uses:

- **pyttsx3** for text-to-speech
- **SpeechRecognition** for speech-to-text
- **pydub** for audio conversion
- **FFmpeg** for processing audio formats
- **asyncio** for asynchronous execution

Audio files are generated and sent as Discord attachments.

The bot does not currently join voice channels or provide live voice communication.

## Project Structure

```text
The-Real-Olrox/
│
├── main.py
├── config.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── commands/
│   ├── __init__.py
│   ├── general.py
│   ├── history.py
│   ├── voice.py
│   ├── weather.py
│   ├── images.py
│   ├── english.py
│   ├── social.py
│   └── levels.py
│   └── economy.py
│
├── models/
│   ├── model.py
│   ├── keras_model.places.h5
│   └── labels.places.txt
│
├── data/
│   └── olrox.db
│
└── assets/
    ├── gifs/
    │   ├── olrox.gif
    │   ├── nice.gif
    │   ├── turning.gif
    │   ├── side_eye.gif
    │   ├── shine.gif
    │   ├── of_course.gif
    │   ├── divider1.gif
    │   ├── divider2.gif
    │   ├── divider3.gif
    │   └── ...
    │
    └── icons/
        ├── sunny.png
        ├── rain.png
        ├── new_moon.png
        └── ...
```

The structure above represents the intended local project layout. Generated files, additional GIFs, and other assets may vary.

**Security:** Keep `config.py` private if it contains credentials. Do not upload the local database, virtual environment, or private tokens.

### Modular Architecture

The bot uses the `discord.py` Cogs system to organize its functionality into separate modules.

| Module | Responsibility |
|---|---|
| `main.py` | Bot initialization and extension loading |
| `general.py` | Greetings, laughter, and random facts |
| `history.py` | Historical information |
| `voice.py` | Text-to-speech generation |
| `weather.py` | Weather and astronomical information |
| `images.py` | Machine learning image classification |
| `english.py` | English practice and speech recognition |
| `social.py` | Member events, profiles, and server information |
| `levels.py` | SQLite XP, level calculation, leaderboards, level-up announcements, and automatic progression roles |
| `models/model.py` | Image preprocessing and model inference |
| `economy.py` | Whole economy system |


This architecture makes the project easier to maintain, debug, test, and expand.

And prevents `main.py` from becoming a 900-year-old monster again.

## Technologies

- Python 3.11
- discord.py
- SQLite (`sqlite3`)
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
- asyncio
- pathlib
-random
-time

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd The-Real-Olrox
```

Replace `<repository-url>` with the actual repository URL.

### 2. Install Dependencies

If the project includes an updated `requirements.txt`:

```bash
pip install -r requirements.txt
```

Alternatively, install the main dependencies:

```bash
pip install discord.py tensorflow pillow numpy SpeechRecognition pydub pyttsx3 requests
```

Install FFmpeg separately and ensure it is available on your system's PATH.

The machine learning feature requires the trained `.h5` model and its corresponding labels file.

### 3. Discord Configuration

1. Create a bot in the Discord Developer Portal.
2. Enable the **Message Content Intent**.
3. Enable the **Server Members Intent** for member join and leave events.
4. Invite the bot to a Discord server with the necessary permissions, including **Manage Roles** for automatic progression roles.
5. Configure the Discord token according to the project's local configuration.
6. Verify that the required models, GIFs, and icons are present.
7. Create the `data/` directory if it does not exist. Configure the progression roles and their IDs in `commands/levels.py`, and place the bot role above them in the server role hierarchy.
8. Run the bot:

```bash
python main.py
```

The SQLite experience table is created automatically when the Levels Cog initializes.

### 4. Optional Server Channels

To enable automatic social messages, create the following text channels:

```text
#bienvenidas
#despedidas
```

The bot must have permission to send messages and embeds in these channels.

**Security:** Never publish Discord bot tokens, passwords, or private API credentials.

## Visual Identity

The bot uses customized Discord embeds featuring:

- Purple accent color (`#74459A`)
- Animated Olrox GIFs
- Weather and moon-phase thumbnails
- Decorative GIF separators
- Avatar-based embed footers
- Sarcastic dialogue and dramatic responses
- Consistent visual styling across commands

The visual identity is inspired by Olrox from *Castlevania: Nocturne*.

## Learning Objectives

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
- Error handling and exception handling
- SQLite databases and SQL queries
- Persistent data storage
- Discord events and permissions
- Command cooldowns and automatic rewards
- Interactive Discord embeds
- Code organization and PEP 8 conventions
- Git and GitHub project documentation

## ⚠️ Limitations

- Weather information depends on `wttr.in`.
- Speech recognition accuracy varies with audio quality.
- Text-to-speech creates audio files, not live voice-channel audio.
- Image classification predictions may be inaccurate.
- Some features require external software or services.
- The bot requires a valid Discord token to run.
- Automatic XP cooldowns reset when the bot restarts.
- Experience data is stored locally and is not automatically synchronized between installations.
- The English game's scores are not currently added to the SQLite XP system.

## Future Development

Potential improvements include:

- An interactive `$help` menu with categorized commands
- Additional historical content and themed interactions
- Additional experience rewards and progression features
- A companion website/dashboard for The Real Olrox
- Expanded server customization
- Improved error handling and configuration

The project continues to evolve as new Python concepts are explored.

---

###  Final Words

What started as a simple Python exercise became a Discord bot with machine learning, audio processing, custom graphics, interactive games, social interactions, and a persistent experience system.

There were errors. There were exceptions. There were questionable decisions.

There were also Git conflicts that probably shortened someone's lifespan.

But I'm trying to survive.

*Constantly fighting for the 1st place.*

**The Real Olrox — because apparently learning Python wasn't dramatic enough.**
