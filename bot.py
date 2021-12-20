import os
import discord
import asyncio
import youtube_dl
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = '$', intents=intents)

# find a way to make it so that this doesnt need to be in the repo lol
TOKEN = "ODE2ODk5OTQ1MjEzODUzNzU2.YEBrXA.l6cSmHJYrzaLM5TQCUJCWt1hDrQ"

youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    #update server list in csv here
    guild = await client.fetch_guild('Volskaya Industries')
    for member in guild.members:
        print(member)

@client.command()
async def join(ctx):
    author = ctx.message.author
    channel = author.voice.channel
    if channel is not None:
        await channel.connect()
    else:
        cxt.send("you have to be in a voice channel for me to join")

@client.command()
async def meow(ctx):
    if ctx.voice_client is None:
        await join(ctx)
    vc = ctx.voice_client
    vc.play(discord.FFmpegPCMAudio('meow.mp3'), after=lambda e: print('done', e))
    
@client.command() 
async def startgamba(ctx, *, nameofbet):
    emojis = ['👍','👎']
    msg = await ctx.send(nameofbet)
    for emoji in emojis:
        await msg.add_reaction(emoji)

@client.command()
async def startbet(ctx, *, nameofbet):
    msg = await ctx.send(nameofbet)
    
@client.command()
async def play( ctx, *, arg ):
    if ctx.voice_client is None:
        await join(ctx)
    
    vc = ctx.voice_client
    if vc is None:
        print("error: no voice client")
    else: 
        if arg.startswith("http"):
            url = arg 
            player = await YTDLSource.from_url(url, stream=True)
            vc.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
        else:
            #search for the video on youtube
            print(arg)
    


client.run(TOKEN)