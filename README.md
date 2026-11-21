# The Real Olrox — Discord Bot

*A sarcastic buddy with a suspicious amount of Python knowledge.*

A Python Discord bot inspired by **Olrox from *Castlevania: Nocturne***. It combines machine learning, English practice, speech recognition, text-to-speech, weather and moon information, historical facts, social interactions, and persistent **SQLite-based experience and economy systems**.

Made by a teenager who's still trying to learn.

Originally developed as a Python learning exercise, the project evolved from one chaotic script into a modular bot built with **discord.py Cogs**.

Nothing serious. Just a vampire learning software engineering. xd

## Features

### General commands

| Command | Description |
|---|---|
| `$hello` | Sarcastic welcome with an animated GIF |
| `$heh` | Repeats “he” a specified number of times |
| `$fact` | Random fact |
| `$history` | Historical information |

### Weather and audio

| Command | Description |
|---|---|
| `$weather <city>` | Weather conditions and an audio report |
| `$night <city>` | Moon phase, sunrise, and sunset |
| `$say <text>` | Converts text into a WAV attachment |

### Interactive features

| Command | Description |
|---|---|
| `$checking` | Classifies images using a trained machine learning model |
| `$english` | Interactive English pronunciation game |

### Social commands

| Command | Description |
|---|---|
| `$profile` | Your Discord server profile |
| `$profile @user` | Another member's profile |
| `$server` | Server information |
| `$testwelcome` | Tests welcome messages (administrator only) |
| `$testgoodbye` | Tests farewell messages (administrator only) |

### Experience and rankings

| Command | Description |
|---|---|
| `$rank` | Your level, XP, and progress |
| `$rank @user` | Another member's progress |
| `$addxp @user <amount>` | Awards XP and synchronizes progression roles (administrator only) |
| `$leaderboard` | Top 10 members by XP |
| `$top` | Alias for `$leaderboard` |

### Treasury and professions

| Command | Description |
|---|---|
| `$balance` | View your Livres and Louis d'or |
| `$daily` | Claim the daily Livres reward |
| `$jobs` | Browse available professions |
| `$job` | Select or manage a profession (see in-bot help for arguments) |
| `$work` | Earn Livres through your profession |
| `$work random` | Perform a random job activity |

### Olrox's Emporium

| Command | Description |
|---|---|
| `$shop` | Browse the paginated shop catalog |
| `$buy <item_id>` | Purchase an item using the appropriate currency |
| `$inventory` | View your collection and item quantities |

### Missions

The bot includes an interactive mission system. The first implemented Revolutionary mission, **The Supply Convoy**, offers choices, outcomes, rewards, and a cooldown. Other profession missions are planned; the full mission catalog is **not** implemented yet. Use the bot's current command help for the available mission entry points.

## Experience and ranking system

The experience system is persistent and server-specific, powered by SQLite.

- Regular eligible messages award **5–15 XP**.
- Each member has a **60-second cooldown** between XP rewards.
- Bot messages and commands beginning with `$` do not generate XP.
- XP remains saved after restarts.
- Levels require progressively more total XP.
- `$rank` shows total XP, a ten-segment progress bar, and XP remaining until the next level.
- Eligible level-ups produce themed embeds and animated GIFs.
- `$addxp` synchronizes progression roles immediately but does not currently send a level-up announcement.

### Automatic progression roles

| Required level | Total XP required | Role |
|---|---:|---|
| 5 | 700 | The Speaker |
| 10 | 2,700 | The Forgemaster |
| 20 | 10,450 | The Dhampir |
| 35 | 31,450 | The Noble |
| 50 | 63,700 | The Vampire Messiah |

These thresholds reflect the existing level calculation in `commands/levels.py`. Progress continues beyond level 50; level 50 is simply the highest configured role. Only one progression role is retained at a time, without affecting unrelated roles. The bot requires **Manage Roles** permission and must have a role above the progression roles.

## Economy, jobs, and inventory

### Two currencies

- **Livres:** the everyday currency used for daily rewards, jobs, and common-market purchases.
- **Louis d'or:** a rare premium in-game currency used for special relics. Routine daily and work rewards do not award it. Special events, administrator rewards, and rare casino jackpots are *planned* acquisition methods, not yet generally implemented.

The daily reward is currently **150 Livres**, with a **24-hour cooldown**. Work and mission activities have their own eligibility rules and cooldowns.

### Professions

Members can choose professions with level requirements and different rewards. The job system includes a catalog of twelve professions, with choices such as Revolutionary, Vampire Informant, Vampire Hunter, Summoner, and other themed occupations. Job changes are restricted by a cooldown, and work rewards are stored persistently.

### Shop and inventory

**Olrox's Emporium** has a paginated catalog of **16 collectible items** across the Common Market (Livres) and Relic Chamber (Louis d'or):

| Item ID | Item | Price | Currency |
|---|---|---:|---|
| `daggers` | Throwing Daggers | 15 | Livres |
| `holy_water` | Holy Water | 40 | Livres |
| `wall_chicken` | Wall Chicken | 75 | Livres |
| `cockade` | Revolutionary Cockade | 120 | Livres |
| `leather_whip` | Leather Whip | 250 | Livres |
| `blood_chalice` | Blood Chalice | 300 | Livres |
| `roses` | Red Roses | 50 | Livres |
| `love_letter` | Love Letter | 25 | Livres |
| `engagement_ring` | Engagement Ring | 1,500 | Livres |
| `pocket_watch` | Pocket Watch | 2 | Louis d'or |
| `grimoire` | Speaker's Grimoire | 5 | Louis d'or |
| `morning_star` | Morning Star | 8 | Louis d'or |
| `familiar` | Maria's Familiar | 12 | Louis d'or |
| `alucard_sword` | Alucard's Sword | 20 | Louis d'or |
| `vampire_killer` | Vampire Killer | 35 | Louis d'or |
| `crimson_stone` | Crimson Stone | 50 | Louis d'or |

Purchases deduct the appropriate balance and update inventory quantities using a SQLite transaction. Items are currently **collectibles**: combat, healing, magical effects, gifting, and marriage/proposal interactions are future features. The Crimson Stone is marked as non-giftable in the catalog.

### SQLite data

The local database is `data/olrox.db`. The currently used tables include:

| Table | Purpose |
|---|---|
| `experience` | XP and level progression by server/member |
| `economy` | Livres, Louis d'or, and daily reward timing |
| `user_jobs` | Selected professions and work timing |
| `active_missions` | Active mission state and related timing |
| `inventory` | Owned item IDs and quantities by server/member |

The inventory table uses `(guild_id, user_id, item_id)` as its composite primary key, preventing duplicate rows for the same owned item. **Do not commit the local database to a public repository.**

## English learning game

The `$english` command helps users practice pronunciation through recorded audio messages.

| Option | Level | Activity | Points per answer |
|---|---|---|---:|
| 1 | Words | Repeat English words | 10 |
| 2 | Sentences | Repeat short sentences | 20 |
| 3 | Translate | Translate Spanish into English | 30 |
| 4 | Challenge | Repeat longer English sentences | 40 |
| 5 | Play All | Complete all four levels | Up to 300 total |

Each level uses three randomly selected questions. Google Speech Recognition transcribes audio, and the bot compares recognized text with expected answers. GIFs accompany responses and transitions. Game scores are currently separate from server XP.

Because Olrox apparently cannot teach English without being dramatic.

## Machine learning

The `$checking` command uses a Google Teachable Machine / Keras model to classify uploaded images as `RESTRICTED` or `NOT RESTRICTED`. It displays the predicted class, confidence score, and confidence description and can generate an audio response. Model assets are kept in `models/`.

**Disclaimer:** This is an experimental educational classifier, not a real security system.

## Weather and moon phases

`$weather` and `$night` use `wttr.in`. Weather output includes conditions, temperature, custom thumbnails, sarcastic commentary, and a text-to-speech report. Night output includes moon phase, sunrise, sunset, and moon-themed thumbnails.

Because even a vampire needs to know when the sun is coming up.

## Social interactions

The `social.py` Cog handles member information and server events. Welcome and farewell embeds can be sent to `#bienvenidas` and `#despedidas`, respectively, with member avatars and decorative GIFs. Administrators can test these events. `$profile` shows member account and server details; `$server` summarizes server information.

## Audio features

- `pyttsx3` for text-to-speech.
- `SpeechRecognition` for speech-to-text.
- `pydub` and FFmpeg for audio conversion.
- `asyncio` for asynchronous operations.

Audio is sent as attachments. The bot does not currently join voice channels or offer live voice conversation.

## Project structure

```text
The-Real-Olrox/
├── main.py
├── config.py
├── README.md
├── requirements.txt
├── .gitignore
├── commands/
│   ├── __init__.py
│   ├── general.py
│   ├── history.py
│   ├── voice.py
│   ├── weather.py
│   ├── images.py
│   ├── english.py
│   ├── social.py
│   ├── levels.py
│   ├── economy.py
│   ├── jobs.py
│   ├── work.py
│   ├── missions.py
│   └── shop.py
├── models/
│   ├── model.py
│   ├── keras_model.places.h5
│   └── labels.places.txt
├── data/
│   └── olrox.db
└── assets/
    ├── gifs/
    │   ├── olrox.gif
    │   ├── nice.gif
    │   ├── snack.gif
    │   ├── richter2.gif
    │   ├── divider1.gif
    │   └── ...
    └── icons/
        ├── sunny.png
        ├── rain.png
        ├── new_moon.png
        └── ...
```

This is the intended project layout; local assets and generated files may vary.

### Modular architecture

| Module | Responsibility |
|---|---|
| `main.py` | Bot initialization and Cog loading |
| `general.py`, `history.py` | General and historical commands |
| `voice.py` | Text-to-speech |
| `weather.py` | Weather and moon information |
| `images.py`, `models/model.py` | Image classification and inference |
| `english.py` | Pronunciation game |
| `social.py` | Member events and profiles |
| `levels.py` | XP, rankings, progression roles |
| `economy.py` | Balances and daily rewards |
| `jobs.py`, `work.py` | Professions and work rewards |
| `missions.py` | Interactive profession missions |
| `shop.py` | Catalog, purchases, and inventory |

This architecture makes the project easier to maintain, debug, test, and expand.

And prevents `main.py` from becoming a 900-year-old monster again.

## Technologies

Python 3.11, discord.py, SQLite (`sqlite3`), TensorFlow/Keras, Google Teachable Machine, NumPy, Pillow, SpeechRecognition, pydub, FFmpeg, pyttsx3, Requests, `wttr.in`, `asyncio`, and `pathlib`.

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd The-Real-Olrox
```

Replace `<repository-url>` with the actual GitHub repository URL.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Alternatively, install the core Python dependencies:

```bash
pip install discord.py tensorflow pillow numpy SpeechRecognition pydub pyttsx3 requests
```

Install FFmpeg separately and add it to your system PATH. Image classification requires the model and labels files.

### 3. Configure Discord

1. Create an application and bot in the Discord Developer Portal.
2. Enable **Message Content Intent**.
3. Enable **Server Members Intent** for join/leave features.
4. Invite the bot with appropriate permissions, including **Manage Roles** for progression roles.
5. Configure the bot token privately according to the local project setup.
6. Ensure required models, GIFs, and icons exist.
7. Create `data/` if needed and configure progression role IDs in `commands/levels.py`.
8. Position the bot's Discord role above the roles it needs to assign.
9. Start the bot:

```bash
python main.py
```

Database tables are initialized by their corresponding modules when the bot starts.

### 4. Optional server channels

Create `#bienvenidas` and `#despedidas` for automatic social messages. Grant the bot permission to send messages and embeds there.

**Security:** Never publish Discord tokens, passwords, private credentials, or `data/olrox.db`. Keep `config.py` private if it contains secrets; use `.gitignore` to prevent accidental commits.

## Visual identity

- Purple accent color: `#74459A`.
- Animated Olrox and *Castlevania*-themed GIFs.
- Custom Discord item and currency emojis.
- Decorative GIF separators.
- Avatar-based embed footers.
- Sarcastic dialogue and dramatic reactions.
- Paginated interactive shop and inventory embeds.

## Learning objectives

Python functions, loops, conditionals, dictionaries, object-oriented programming, Cogs, asynchronous code, external APIs, machine learning, audio processing, file management, error handling, SQL, transactions, persistent state, Discord permissions, cooldowns, buttons, PEP 8, Git, and GitHub documentation.

## Limitations

- Weather information depends on `wttr.in`.
- Speech recognition depends on audio quality.
- Text-to-speech produces audio attachments, not live voice-channel audio.
- Image predictions may be inaccurate.
- Some features require external programs or services.
- XP cooldowns may reset when the bot restarts.
- The database is local and is not automatically synchronized across installations.
- English game points are separate from SQLite XP.
- Shop items do not yet have gameplay effects.
- Gifts, player-to-player transfers, robberies, and casino games are not yet implemented.

## Development roadmap

The project follows a 28-day development plan. Current economy milestones:

| Day | Focus | Status |
|---|---|---|
| 04 | Treasury: Livres, Louis d'or, `$balance`, `$daily` | Implemented |
| 05 | Professions: `$jobs`, `$job`, `$work` | Implemented |
| 06 | Shop and inventory: `$shop`, `$buy`, `$inventory` | Implemented |
| 07 | Gifts and secure transfers | Planned |
| 08 | Robberies, fines, protection | Planned |
| 09 | Casino: `$coinflip`, `$dice`, and proposed blackjack (21) | Planned |
| 10 | Economic balancing, visual polish, error handling, README | Planned |

Additional planned work includes a reusable mission engine, expanded profession missions, item effects, a possible romantic proposal feature, rare Louis d'or event rewards and casino jackpots, an interactive `$help`, and a companion website/dashboard in the final development week.

## Final words

What started as a simple Python exercise became a Discord bot with machine learning, audio processing, custom graphics, interactive games, social interactions, and persistent experience and economy systems.

There were errors. There were exceptions. There were questionable decisions.

There were also Git conflicts that probably shortened someone's lifespan.

But I'm trying to survive.

*Constantly fighting for the 1st place.*

**The Real Olrox — because apparently learning Python wasn't dramatic enough.**
