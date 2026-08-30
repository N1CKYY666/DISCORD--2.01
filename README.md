# Discord Image Classification Bot

This project is a **Discord bot** that can receive images from users and classify them using a machine learning model created with **Google Teachable Machine** and **Keras**.

The bot was created as a practice project to combine **Discord commands**, **Python**, and an **image classification model**.

> **Disclaimer:** This model classifies places as **RESTRICTED** or **NOT RESTRICTED**.

---

## Features

The bot includes several commands that allow users to interact with it.

### `$hello`

The bot sends a greeting message.

Example:

```text
$hello
```

### `$heh`

The bot repeats `"he"` a specified number of times.

Example:

```text
$heh 5
```

### `$checking`

The user sends an image as an attachment together with the command.

The bot downloads the image, analyzes it using the trained Keras model, and returns the **predicted class** and **confidence score**.

Example:

```text
$checking
```

Attach an image of a place when sending the command.

---

## Project Files

The project contains the following files:

```text
project/
│
├── bot.py
├── model.py
├── keras_model.h5
├── labels.txt
└── README.md
```

### `bot.py`

Contains the Discord bot configuration and commands.

The bot receives images through Discord and sends them to the `get_class()` function for classification.

### `model.py`

Contains the `get_class()` function.

This function:

1. Loads the Keras model.
2. Loads the class labels.
3. Opens the image.
4. Resizes the image to **224 × 224 pixels**.
5. Converts the image into a NumPy array.
6. Normalizes the image.
7. Sends the image to the model.
8. Returns the predicted class and confidence score.

### `keras_model.h5`

Machine learning model exported from **Google Teachable Machine**.

### `labels.txt`

Contains the names of the classes that the model can recognize:

```text
RESTRICTED
NOT RESTRICTED
```

---

## Requirements

This project uses **Python 3.11**.

> **Important:** Python 3.11 is recommended for this project.

Install the required libraries using:

```bash
pip install discord.py
pip install numpy
pip install keras
pip install requests
pip install tensorflow==2.12.0
pip install Pillow
```

> **Important:** Use TensorFlow `2.12.0`. Other versions may cause compatibility problems with the project.

---

## How to Run the Bot

1. Create a Discord bot in the **Discord Developer Portal**.
2. Obtain the bot token.
3. Place the token in the bot configuration.
4. Make sure `keras_model.h5` and `labels.txt` are in the project folder.
5. Install all the required libraries.
6. Run `bot.py`.

```bash
python bot.py
```

When the bot connects successfully, the terminal will display:

```text
We have logged in as BOT_NAME
```

---

## Image Classification Example

To classify an image, send the image in Discord together with:

```text
$checking
```

The bot will process the image and determine whether the place is classified as **RESTRICTED** or **NOT RESTRICTED**.

It will also return the confidence score of the prediction.

Example output:

```text
Class: RESTRICTED
Confidence Score: 0.98
```

---

## Technologies Used

* Python 3.11
* Discord.py
* TensorFlow
* Keras
* NumPy
* Pillow
* Google Teachable Machine

---

## Security Note

**Never upload your Discord bot token to GitHub.**

Avoid publishing code containing your real token:

```python
bot.run("YOUR_REAL_TOKEN")
```

If your token is uploaded publicly, other people could use it to control your bot.

For a real project, it is better to store the token in an **environment variable** or a `.env` file and add that file to `.gitignore`.

---

## Purpose

This project was developed as a learning exercise to practice:

* Discord bot development.
* Python functions.
* Image processing.
* Machine learning model integration.
* Image classification with Keras.
* Using a Teachable Machine model inside a Python application.

---

## Author

Developed as a practice project for learning **Python, Discord bots, and machine learning**.
