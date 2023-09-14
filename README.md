# AzureTTVChat

AzureTTVChat Chat is a Python Script that gives a random twitch chatter a tts voice.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install **pipenv**.

```bash
pip install pipenv
```
after that use this command to install the dependencies.
```bash
pipenv install --dev
```
this will install the packages specified in the **Pipfile**.
## Usage
first fill the environment file with your data
```env
TWITCH_TOKEN= #oauthtoken you can get a test one at twitchtokengenerator.com
TWITCH_CHANNEL= #your twitch channel
PREFIX= #prefix of command play
SPEECH_KEY= #key from speech studio
SPEECH_REGION= #region from speech studio
KEYPRESS= #key that runs choose function
```
before you run the script make sure that your terminal is in the project directory before executing if not change these lines to the absolute path to these XML files
```python
    default_voice = open("default.xml", "r").read()

    angry = open("angry.xml", "r").read()

    cheerful = open("cheerful.xml", "r").read()

    excited = open("excited.xml", "r").read()

    sad = open("sad.xml", "r").read()

    friendly = open("friendly.xml", "r").read()

    hopeful = open("hopeful.xml", "r").read()

    shouting = open("shouting.xml", "r").read()

    whispering = open("whispering.xml", "r").read()

    terrified = open("terrified.xml", "r").read()

    unfriendly = open("unfriendly.xml", "r").read()
```
then run this command in the terminal
```bash
pipenv run python twitchazurechatbot.py
```
