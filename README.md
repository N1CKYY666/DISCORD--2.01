# DISCORD-- IMAGE CLASIFICATION

This project is a Discord bot that can receive images from users and classify them using a machine learning model created with Teachable Machine and Keras.
The bot was created as a practice project to combine Discord commands with an image classification model! 

DISCLAIMER : ONLY SPARROW OR PIGEONS INMAGES.

Here you have some features:

Commands included:

$hello
The bot sends a greeting message.

$heh
The bot repeats "he" a specified number of times.

  Example:
  text
  $heh 5
  
$checking
  The user sends an image as an attachment together with the command. The bot downloads the image, analyzes it using the trained Keras model, and returns the predicted class and confidence score.

Project files

This project contains these files:

  text
project/
│
├── bot.py
├── model.py
├── keras_model.h5
├── labels.txt
└── README.md


----bot.py
Contains the Discord bot configuration and commands. The bot receives images through Discord and sends them to the get_class() function for classification.

----model.py
Contains the get_class() function.

This function:

1. Loads the Keras model.
2. Loads the class labels.
3. Opens the image.
4. Resizes the image to 224 x 224 pixels.
5. Converts the image into a NumPy array.
6. Normalizes the image.
7. Sends the image to the model.
8. Returns the predicted class and confidence score.

----keras_model.h5
Machine learning model exported from Teachable Machine.

----labels.txt
Contains the names of the classes that the model can recognize. (Pigeons or sparrows)

----Requirements
The project uses Python and the following libraries, this will ensure the bot is working well;

pip install discord.py
pip install numpy
pip install keras
pip install requests
pip install tensorflow==2.12.0 (USE THIS VERSION! Another versions may give you problems with VS code)
pip install Pillow


----How to run the bot

1. Create a Discord bot in the Discord Developer Portal.
2. Obtain the bot token.
3. Place the token in the bot configuration.
4. Make sure keras_model.h5 and labels.txt are in the project folder.
5. Run!

When the bot connects successfully, the terminal will display:

We have logged in as BOT_NAME

----Example

To classify an image of PIGEONS and SPARROWS, send an image in Discord together with:


$checking


The bot will process the image and return the predicted class and its confidence score.

----Technologies used

  Python
  Discord.py
  TensorFlow / Keras
  NumPy
  Pillow
  Google Teachable Machine

----Security note

The Discord bot token should not be uploaded to GitHub

Instead of writing the real token directly in the code:
bot.run("tokenazo")


## Purpose

This project was developed as a learning exercise to practice:

* Discord bot development.
* Python functions.
* Image processing.
* Machine learning model integration.
* Image classification with Keras.

python version: 3.11 (USE THIS ONE)



