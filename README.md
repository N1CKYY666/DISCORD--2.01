# The Real Olrox — Discord Bot

A Python Discord bot inspired by **Olrox from Castlevania: Nocturne**, combining machine learning, English learning, speech recognition, text-to-speech, weather information, and a very sarcastic vampire personality. xd

The project was developed as a Python learning exercise, exploring Discord commands, image classification, audio processing, external APIs, dictionaries, and customized Discord embeds. Nothing serious 

## Features

### `$hello` — An Unexpected Visitor

Displays a personalized greeting using a purple Discord embed and an animated Olrox GIF thumbnail.

**Example:**
```text
$hello
```

The bot welcomes the user with a sarcastic message inspired by Olrox's personality.

### `$heh` — Laughing Command

Repeats `"he"` a specified number of times.

**Example:**
```text
$heh 5
```

### `$say` — Text-to-Speech

Converts a user's text into a WAV audio file using `pyttsx3`.

**Example:**
```text
$say Hello, mortal.
```

- Supports messages up to 200 characters.
- Generates audio using a configured voice and speaking rate.
- Sends the audio file directly to the Discord text channel.

The bot does not automatically join voice channels.

### `$checking` — Image Classification

Uses a machine learning model trained with Google Teachable Machine and Keras to classify uploaded images.

**Example:**
```text
$checking
```

Attach an image to the command.

The bot:

1. Downloads the attached image.
2. Processes it using the trained model.
3. Identifies whether the image belongs to `RESTRICTED` or `NOT RESTRICTED`.
4. Displays the predicted class, probability, and confidence description.
5. Generates a spoken warning or confirmation using `pyttsx3`.

**Example result:**
```text
Zone: RESTRICTED
Probability: 98.5%
Confidence: High confidence

WARNING: This is a restricted area!
```

**Disclaimer:** This classification model is experimental and must not be used as a real security system.

### `$english` — English Learning Game

An interactive game that allows users to practice English pronunciation through recorded audio.

**Example:**
```text
$english
```

The bot displays five options:

| Option | Level | Activity | Points per correct answer |
|---|---|---|---|
| 1 | Words | Repeat English words | 10 |
| 2 | Sentences | Repeat short sentences | 20 |
| 3 | Translate | Translate Spanish words into English | 30 |
| 4 | Challenge | Repeat longer English sentences | 40 |
| 5 | Play All | Complete all four levels | Up to 300 total |

Each level randomly selects three questions.

The bot uses `SpeechRecognition` to transcribe audio and compare the recognized text against the expected answer.

**Maximum score:** 300 points.

### `$weather` — The Mortal Forecast

Retrieves current weather information from the `wttr.in` service.

**Example:**
```text
$weather London
```

The bot displays:

- Requested location
- Current weather condition
- Temperature
- A randomly selected sarcastic comment
- A custom weather thumbnail when a matching icon is available

Weather results are displayed in a purple Discord embed.

The bot also uses `pyttsx3` to generate an audio report.

**Example output:**
```text
─── THE MORTAL FORECAST ───

Location: London
Weather: Partly Cloudy
Temperature: +8°C

"Centuries of wisdom, wasted on weather reports."
```

Weather conditions are associated with local PNG images through a Python dictionary.

### `$night` — The Vampire's Forecast

Retrieves astronomical information from `wttr.in`.

**Example:**
```text
$night London
```

The command displays:

- Current moon phase
- Sunrise time
- Sunset time
- A sarcastic comment inspired by Olrox
- A custom moon-phase thumbnail

**Example output:**
```text
─── NIGHTS FORECAST ───

Location: London
Moon phase: 🌕
Sunrise: 07:39:27
Sunset: 17:49:43

"The sun is finally leaving. I can visit Mizrak."
```

The bot identifies the moon phase returned by `wttr.in` and selects the corresponding PNG using a Python dictionary.

Eight moon phases are supported:

1. New Moon
2. Waxing Crescent
3. First Quarter
4. Waxing Gibbous
5. Full Moon
6. Waning Gibbous
7. Last Quarter
8. Waning Crescent

## Custom Discord Embeds

The bot uses `discord.Embed()` to display customized messages.

Visual elements include:

- Purple accent color (`#74459A`)
- Decorative titles using `───`
- Organized weather and astronomical information
- Custom thumbnails
- Sarcastic descriptions and footers

The visual style is inspired by Olrox's appearance and personality in *Castlevania: Nocturne*.

## Custom Icons

The project includes custom PNG icons designed to match the bot's visual identity.

Icons are stored in:

```text
olrox_all_icons/
    images/
        new_moon.png
        waxing_crescent.png
        first_quarter.png
        waxing_gibbous.png
        full_moon.png
        waning_gibbous.png
        last_quarter.png
        waning_crescent.png
        ...
```

Additional icons represent weather conditions such as sunny, cloudy, rainy, snowy, and windy weather.

Python dictionaries connect API responses to image filenames. The bot attaches the matching PNG and displays it using `embed.set_thumbnail()`.

If no matching icon is available, the embed can still be displayed without a thumbnail.

## Speech Recognition

The English learning game uses:

- `SpeechRecognition` for speech-to-text conversion
- `pydub` for audio conversion
- Google Speech Recognition for transcription
- FFmpeg for processing supported audio formats

The bot downloads the user's audio attachment, converts it to WAV, and transcribes the recording.

The recognized text is compared with the expected answer to calculate the score.

## Text-to-Speech

The bot uses `pyttsx3` for speech synthesis.

The `create_voice()` function configures the voice, speaking rate, and volume before saving the generated audio to a WAV file.

Text-to-speech is currently used by:

- `$say`
- `$checking`
- `$weather`

Audio generation is executed using `asyncio.to_thread()` to avoid blocking the Discord event loop while the synchronous speech engine is running.

## Technologies

- Python
- discord.py
- Google Teachable Machine
- TensorFlow / Keras
- Pillow
- NumPy
- SpeechRecognition
- pydub
- FFmpeg
- pyttsx3
- Requests
- wttr.in

## Installation

Install the required Python packages:

```bash
pip install discord.py tensorflow pillow numpy SpeechRecognition pydub pyttsx3 requests
```

Install FFmpeg separately and make sure it is available on your system's PATH for audio conversion.

The image classification feature also requires the trained Keras model and its labels file.

## Configuration

1. Create a Discord application and bot in the Discord Developer Portal.
2. Enable the Message Content Intent.
3. Invite the bot to your server with the necessary permissions.
4. Add the trained image classification model and labels.
5. Place the custom icons in the expected folder.
6. Configure the Discord bot token securely.
7. Run the Python script.

For improved security, the bot token should be loaded from an environment variable instead of being written directly into the source code.

## Example Commands

```text
$hello
$heh 5
$say Good evening, mortal.
$checking
$english
$weather London
$night London
```

## Project Structure

```text
The-Real-Olrox/
│
├── main.py
├── model.py
├── keras_model.places.h5
├── labels.places.txt
├── olrox.gif
├── README.md
│
└── olrox_all_icons/
    └── images/
        ├── new_moon.png
        ├── waxing_crescent.png
        ├── first_quarter.png
        ├── waxing_gibbous.png
        ├── full_moon.png
        ├── waning_gibbous.png
        ├── last_quarter.png
        ├── waning_crescent.png
        └── other_weather_icons.png
```

The final weather icon filenames should match the names referenced in the Python dictionary.

## Learning Objectives

This project demonstrates practical applications of:

- Python functions, loops, conditionals, and dictionaries
- Asynchronous Discord commands
- External HTTP requests and API responses
- Machine learning inference
- Image processing
- Audio recording and conversion
- Speech recognition
- Speech synthesis
- Temporary file management
- Customized Discord embeds
- File paths and asset management

## Limitations

- Weather information depends on the availability and accuracy of `wttr.in`.
- Some weather conditions may not have a matching custom thumbnail.
- Speech recognition accuracy depends on audio quality and pronunciation.
- Text-to-speech generates audio attachments rather than live voice-channel speech.
- Image classification results are predictions and may be inaccurate.
- The bot requires a valid Discord token and its external dependencies.

---

*Constantly fighting for the 1st place*
