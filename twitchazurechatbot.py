import requests
import webbrowser
import time
import twitchio
from twitchio.ext import commands
import random
import os
import azure.cognitiveservices.speech as speechsdk
import re
import asyncio
import keyboard
from flask import Flask, render_template, request, redirect , jsonify
import threading
from flask_socketio import SocketIO, emit


CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:5000/tokenauth'

def get_twitch_auth_url():
    return f"https://id.twitch.tv/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=chat:read+chat:edit"

def open_auth_url():
    webbrowser.open(get_twitch_auth_url())

def get_auth_token(code):
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI
    }
    response = requests.post('https://id.twitch.tv/oauth2/token', data=data)
    return response.json()['access_token']

app = Flask(__name__)
socketio = SocketIO(app)

moderation_queue = []

@app.route('/tokenauth')
def tokenauth():
    twitch_code = request.args.get('code')
    token = get_auth_token(twitch_code)
    write_token_to_env(token)
    return "Authorization successful"


class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(token=os.environ.get('TWITCH_TOKEN'), prefix=os.environ.get('PREFIX'),initial_channels=[os.environ.get('TWITCH_CHANNEL')])
        self.playing_chatters: list[str] = [] 
        self.selected_chatter: str | None = None
        self.ready_to_process_messages = False
        keyboard.add_hotkey(os.environ.get('KEYPRESS'), self.handle_key)


    async def event_ready(self) -> None:
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    @commands.command()
    async def play(self, ctx: commands.Context):
        print("Play invoke")
        self.playing_chatters.append(ctx.author.name)
        await ctx.send(f'{ctx.author.name} wants to play!')


    async def choose(self):
        print("Choose invoke")
        channel = self.get_channel(os.environ.get('TWITCH_CHANNEL'))
        if self.playing_chatters:
            self.selected_chatter = random.choice(self.playing_chatters)
        
            await channel.send(f'{self.selected_chatter} has been selected!')
            self.ready_to_process_messages = True
        else:
            await channel.send('No users have used the !play command yet.')

    def handle_key(self):
        asyncio.run_coroutine_threadsafe(self.choose(), self.loop)

    async def event_message(self, message: twitchio.Message):
        if message.echo:
                return
        if self.ready_to_process_messages and self.selected_chatter is not None:
            if message.author.name == self.selected_chatter:
                moderation_queue.append(message.content)
                socketio.emit('update', moderation_queue)
        await self.handle_commands(message)

        

        


def extract_parentheses(text):
    pattern = r'^\((.*?)\)'
    match = re.search(pattern, text)
    
    if match:
        inside_parentheses = match.group(1)
        text = text.replace(match.group(0), '')
        return inside_parentheses, text
    else:
        return "default", text

def synthesizer_with_style(chatmessage):
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_config.speech_synthesis_voice_name = 'en-US-DavisNeural'
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    styleinput, twitch_text = extract_parentheses(chatmessage)
    styleinput = styleinput.lower()
    styledegree="2"
    voice = "en-US-DavisNeural"
    role = "OlderAdultMale"
    text = (f'<speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" '
            f'xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US"><voice name="{voice}"><s '
            f'/><mstts:express-as style="{styleinput}" styledegree="{styledegree}" role="{role}">{twitch_text}'
            f'</mstts:express-as><s /></voice></speak>')


    speech_synthesis_result = speech_synthesizer.speak_ssml_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

@app.route('/', methods=['GET', 'POST'])
def moderation():
    if request.method == 'POST':
        if 'allow' in request.form:
            if moderation_queue:
                message = moderation_queue.pop(0)
                if message is not None:
                    synthesizer_with_style(message)
                    socketio.emit('update', moderation_queue)
        elif 'deny' in request.form and moderation_queue:
            moderation_queue.pop(0)
            socketio.emit('update', moderation_queue)
        return redirect('/')
    return render_template('moderation.html')



@app.route('/get_messages', methods=['GET'])
def get_messages():
    if moderation_queue:
        message = moderation_queue[0]
    else:
        message = None
    return jsonify(message=message)

def write_token_to_env(token):
    with open('.env', 'r') as f:
        lines = f.readlines()

    with open('.env', 'w') as f:
        for line in lines:
            if line.startswith('TWITCH_TOKEN'):
                f.write(f'TWITCH_TOKEN="{token}"\n')
            else:
                f.write(line)


if __name__ == '__main__':

    thread = threading.Thread(target=app.run)
    thread.daemon = True
    thread.start()
    if not os.environ.get('TWITCH_TOKEN'):
        open_auth_url()
        time.sleep(6)
    bot = Bot()
    bot.run()