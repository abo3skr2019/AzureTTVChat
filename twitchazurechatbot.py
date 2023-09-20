import twitchio
from twitchio.ext import commands
import random
import os
import azure.cognitiveservices.speech as speechsdk
import re
import asyncio
import keyboard


class Bot(commands.Bot):

    def __init__(self) -> None:
        super().__init__(token=os.environ.get('TWITCH_TOKEN'), prefix=os.environ.get('PREFIX'), channel=[os.environ.get('TWITCH_CHANNEL')])
        self.playing_chatters: list[str] = [] 
        self.selected_chatter: str | None = None
        self.ready_to_process_messages = False
        keyboard.on_press_key('KEYPRESS', self.handle_key)


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
        channel = self.get_channel(channel)
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
                await asyncio.to_thread(synthesizer_with_style, message.content)
        await self.handle_commands(message)

        

        


def extract_parentheses(text):
    pattern = r'^\((.*?)\)'
    match = re.search(pattern, text)
    
    if match:
        inside_parentheses = match.group(1)
        text = text.replace(match.group(0), '')
        return inside_parentheses, text
    else:
        return None, text

def synthesizer_with_style(chatmessage):
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    audio_config = speechsdk.audio.AudioOutputConfig(device_name="{0.0.0.00000000}.{f6aeced4-ff02-42f6-9faf-946d2911aba3}")
    speech_config.speech_synthesis_voice_name = 'en-US-DavisbaNeural'
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

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

    styleinput, twitch_text = extract_parentheses(chatmessage)
    
    if styleinput.lower() == "angry":
        style = angry
    elif styleinput.lower() == "cheerful":
        style = cheerful
    elif styleinput.lower() == "excited":
        style = excited
    elif styleinput.lower() == "sad":
        style = sad
    elif styleinput.lower() == "friendly":
        style = friendly
    elif styleinput.lower() == "hopeful":
        style = hopeful
    elif styleinput.lower() == "shouting" :
        style = shouting
    elif styleinput.lower() == "whispering":
        style = whispering
    elif styleinput.lower() == "terrified":
        style = terrified
    elif styleinput.lower() == "unfriendly":
        style = unfriendly
    else:
        style = default_voice

    text = style + twitch_text + "</mstts:express-as><s /></voice></speak>"
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



bot = Bot()
bot.run()
