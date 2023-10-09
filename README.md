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
TWITCH_TOKEN=             #oauthtoken you can get a test one at twitchtokengenerator.com
TWITCH_CHANNEL=           #your twitch channel
PREFIX=                   #prefix of command play
SPEECH_KEY=               #key from speech studio
SPEECH_REGION=            #region from speech studio
KEYPRESS=                 #key that runs choose function
```
then run this command in the terminal
```bash
pipenv run python twitchazurechatbot.py
```
TTS Should work You may want to use a different voice or style how you do that is by editing these variables
```python
    styleinput = styleinput.lower()
    styledegree="2"
    voice = "en-US-DavisNeural"
    role = "OlderAdultMale"
```
you can find out more about these [here](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-synthesis-markup-voice) 
