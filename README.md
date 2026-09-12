# Discord Image Classification & English Learning Bot

This project is a **Discord bot** developed in Python that combines two main features:

1. **Image classification** using a machine learning model created with **Google Teachable Machine** and **Keras**.
2. An **English learning game** that allows users to practice words, sentences, and translations using voice recordings.

The project was created as a practice exercise to combine **Discord commands, Python, machine learning, image processing, and speech recognition**.

> **Disclaimer:** The image classification model classifies places as **RESTRICTED** or **NOT RESTRICTED**.

---

## Features

The bot includes several commands that allow users to interact with it.

### `$hello`

The bot sends a greeting message.

Example:

```text
$hello
```

---

### `$heh`

The bot repeats `"he"` a specified number of times.

Example:

```text
$heh 5
```

---

### `$checking`

The user sends an image as an attachment together with the command.

The bot downloads the image, analyzes it using the trained Keras model, and returns the **predicted class** and **confidence score**.

Example:

```text
$checking
```

Attach an image of a place when sending the command.

Possible output:

```text
Zone: RESTRICTED
Probability: 98.5%

WARNING: This is a restricted area.
```

or:

```text
Zone: NOT RESTRICTED
Probability: 97.2%

No problem detected. This area is not restricted.
```

---

### `$english`

Starts the **English Learning Game**.

Example:

```text
$english
```

The bot displays four options:

```text
1. Level 1 - Words
2. Level 2 - Sentences
3. Level 3 - Translate
4. Play all
```

The user selects a level by typing the corresponding number.

---

## English Game

The English Game contains three difficulty levels.

### Level 1 - Words

The bot displays an English word and asks the user to repeat it.

Examples:

```text
apple
house
coffee
teacher
chicken
```

Each correct answer gives:

```text
10 points
```

---

### Level 2 - Sentences

The bot displays a short English sentence.

Examples:

```text
good morning
I like coffee
I have a dog
I am a student
```

The user must pronounce the sentence correctly.

Each correct answer gives:

```text
20 points
```

---

### Level 3 - Translate

The bot displays a word in Spanish.

Examples:

```text
casa
perro
gato
agua
escuela
```

The user must say the English translation.

Examples:

```text
casa → house
perro → dog
gato → cat
```

Each correct answer gives:

```text
30 points
```

---

### Play All

Option `4` allows the user to play all three levels.

The final score is calculated by adding the points obtained in every level.

Example:

```text
Your final score: 180
```

---

## Voice Recognition

The English Game uses **SpeechRecognition** to convert the user's recorded audio into text.

The bot:

1. Receives an audio file or Discord voice message.
2. Downloads the audio.
3. Converts the audio to WAV when necessary.
4. Reads the audio using `SpeechRecognition`.
5. Uses Google Speech Recognition with English (`en-US`).
6. Converts the recognized text to lowercase.
7. Compares the recognized answer with the expected answer.
8. Awards points when the answer is correct.

Example:

```text
Word: teacher

User audio:
"teacher"

Bot:
You said: teacher
Correct!
```

> **Note:** The bot does not directly record the user's computer microphone. The user must send a supported audio file or voice message through Discord.

---

## Project Files

The project contains the main bot files and the machine learning model:

```text
project/
│
├── main.py
├── model.py
├── keras_model.places.h5
├── labels.places.txt
├── README.md
└── .gitignore
```

Additional temporary audio files may be created while the English Game is running.

---

## `main.py`

Contains the main Discord bot configuration and commands.

It includes:

* Discord bot configuration.
* `$hello` command.
* `$heh` command.
* `$checking` command.
* `$english` command.
* Image attachment handling.
* Audio attachment handling.
* English Game levels.
* Score calculation.
* Speech recognition.

---

## `model.py`

Contains the `get_class()` function used by the image classification system.

This function:

1. Loads the Keras model.
2. Loads the class labels.
3. Opens the image.
4. Resizes the image to **224 × 224 pixels**.
5. Converts the image into a NumPy array.
6. Normalizes the image.
7. Sends the image to the model.
8. Returns the predicted class and confidence score.

---

## Machine Learning Model

The image classification model was created using **Google Teachable Machine**.

The model recognizes two classes:

```text
RESTRICTED
NOT RESTRICTED
```

The trained model is stored in:

```text
keras_model.places.h5
```

The class names are stored in:

```text
labels.places.txt
```

---

## Requirements

This project uses **Python 3.11**.

> **Important:** Python 3.11 is recommended for compatibility with the machine learning libraries used in this project.

Install the required Python libraries:

```bash
pip install discord.py
pip install numpy
pip install keras
pip install requests
pip install tensorflow==2.12.0
pip install Pillow
pip install SpeechRecognition
pip install pydub
```

---

## FFmpeg

The English Game uses **pydub** to process audio files.

For this reason, **FFmpeg must also be installed on the computer**.

On Windows, FFmpeg can be installed using:

```powershell
winget install Gyan.FFmpeg
```

After installing FFmpeg, restart the terminal or Visual Studio Code.

Check that FFmpeg is available with:

```powershell
ffmpeg -version
```

If FFmpeg is installed correctly, information about the installed version will be displayed.

---

## How to Run the Bot

### 1. Create the Discord bot

Create an application and bot using the **Discord Developer Portal**.

Obtain the bot token and invite the bot to your Discord server.

---

### 2. Install the dependencies

Install the required Python libraries and FFmpeg.

---

### 3. Add the machine learning files

Make sure these files are located in the project folder:

```text
keras_model.places.h5
labels.places.txt
```

---

### 4. Configure the Discord token

For security reasons, the Discord token should not be written directly in the Python source code.

The bot reads the token from an environment variable called:

```text
DISCORD_TOKEN
```

For example, in PowerShell:

```powershell
$env:DISCORD_TOKEN="YOUR_DISCORD_BOT_TOKEN"
```

---

### 5. Run the bot

Run:

```bash
python main.py
```

When the bot connects successfully, the terminal will display:

```text
We have logged in as BOT_NAME
```

---

## Commands Summary

| Command | Function |
|---|---|
| `$hello` | Sends a greeting |
| `$heh 5` | Repeats `"he"` a specified number of times |
| `$checking` | Classifies an attached image |
| `$english` | Starts the English Learning Game |

---

## Technologies Used

* Python 3.11
* Discord.py
* TensorFlow
* Keras
* NumPy
* Pillow
* Google Teachable Machine
* SpeechRecognition
* Google Speech Recognition
* pydub
* FFmpeg

---

## Security

**Never upload your real Discord bot token to GitHub.**

Do not publish code containing:

```python
bot.run("YOUR_REAL_TOKEN")
```

Instead, use an environment variable:

```python
import os

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
```

Files containing passwords, tokens, credentials, or other private information should also be included in `.gitignore`.

If a Discord bot token is accidentally published, it should be **regenerated immediately**.

---

## Purpose

This project was developed as a learning exercise to practice:

* Discord bot development.
* Python functions.
* Conditional statements and loops.
* Dictionaries and lists.
* Random question selection.
* File handling.
* Image processing.
* Machine learning model integration.
* Image classification with Keras.
* Audio processing.
* Speech recognition.
* User interaction through Discord.
* Basic cybersecurity practices.

---

## Author

Developed as a practice project for learning **Python, Discord bots, machine learning, image classification, and speech recognition**.
