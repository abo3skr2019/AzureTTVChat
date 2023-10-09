# AzureTTVChat

AzureTTVChat is a Python Script that gives a random twitch chatter a tts voice.

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
then run this command in the terminal
```bash
pipenv run python twitchazurechatbot.py
```
