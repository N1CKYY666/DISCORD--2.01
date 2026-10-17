# Discord Image Classification, English Learning & Text-to-Speech Bot

This project is a **Discord bot** developed in Python that combines three main features:

1. **Image classification** using a machine learning model created with **Google Teachable Machine** and **Keras**.
2. An **English learning game** that allows users to practice words, sentences, and translations using voice recordings.
3. **Text-to-Speech (TTS)** using `pyttsx3`, allowing the bot to generate spoken messages and audio alerts.

The project was created as a practice exercise to combine **Discord commands, Python, machine learning, image processing, speech recognition, and speech synthesis**.

> **Disclaimer:** The image classification model predicts whether a place belongs to the RESTRICTED or NOT RESTRICTED class. Predictions are not guaranteed to be accurate and should not be used as a real security system.

---

## Features

### `$hello`

The bot sends a greeting message.

```text
$hello
```

### `$heh`

The bot repeats "he" a specified number of times.

```text
$heh 5
```

### `$say` — Text-to-Speech

The user writes a message, and the bot converts it into a spoken audio file using `pyttsx3`.

Example:

```text
$say Hello humans! I am your little robot!
```

The bot generates a WAV audio file and sends it to the Discord channel.

The command supports messages up to 200 characters.

### `$checking` — Image Classification with Voice Alerts

The user sends an image as an attachment together with the command.

The bot:

1. Downloads the attached image.
2. Analyzes it using the trained Keras model.
3. Returns the predicted class and confidence score.
4. Generates a voice message using `pyttsx3`.
5. Sends the audio file to the Discord channel.

Example:

```text
$checking
```

Attach an image when sending the command.

**Possible result 1:**

```text
Zone: RESTRICTED
Probability: 98.5%

WARNING: This is a restricted area!
```

The bot also generates an audio file saying:

"WARNING! RESTRICTED AREA!"

**Possible result 2:**

```text
Zone: NOT RESTRICTED
Probability: 97.2%

No problem detected. This area is not restricted.
```

The bot generates an audio file saying:

"No problem detected. This area is not restricted."

> The bot sends WAV audio files in the text channel. It does not automatically join a Discord voice channel.

### `$english` — English Learning Game

Starts an interactive English learning game using voice recognition.

```text
$english
```

The bot displays five options:

```text
1. Level 1 - Words
2. Level 2 - Sentences
3. Level 3 - Translate
4. Level 4 - Challenge
5. Play all
```

The user selects a level by typing the corresponding number.

---

## English Learning Game

The English Game contains four difficulty levels.

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

Each correct answer awards **10 points**.

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

Each correct answer awards **20 points**.

### Level 3 - Translate

The bot displays a Spanish word, and the user must say its English translation.

Examples:

```text
casa → house
perro → dog
gato → cat
agua → water
escuela → school
```

Each correct answer awards **30 points**.

### Level 4 - Challenge

The bot displays longer and more complex English sentences.

Examples:

```text
I usually wake up early
The weather is beautiful today
I would like a cup of coffee
My favorite subject is English
I am learning how to speak English
```

The user must repeat the complete sentence using a voice message.

Each correct answer awards **40 points**.

### Play All

Option `5` allows the user to complete all four levels.

Each level randomly selects three questions.

The final score is calculated by adding the points obtained in each level.

**Maximum possible score: 300 points.**

```text
Your final score: 300
```

---

## Speech Recognition

The English Game uses **SpeechRecognition** to convert recorded audio into text.

The bot:

1
