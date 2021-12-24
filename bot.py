import os
import re
import discord
import asyncio
import youtube_dl
import urllib.request
import urllib.parse
import random
import csv
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient

load_dotenv('.env')

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = '$', intents=intents)

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
    memberList = client.get_guild(842188551646347264).members
    addList = list()
    fileList = list()
    with open('memberpoints.csv', mode = 'r') as file:
        fReader = csv.reader(file)
        for row in fReader:
            fileList.append(row[0])
        for member in memberList:
            w = 0
            for fileMembers in fileList:
                if (member.name == fileMembers) :
                    w = 1
            if (w == 0) :
                addList.append(member)
            w = 0
    with open('memberpoints.csv', mode  = 'a', newline = '') as file:
        fWriter = csv.writer(file)
        for i in addList:
            row = [i.name,0]
            fWriter.writerow(row)

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
async def coinflip(ctx):
    a = random.random()
    emojis = ['👍','👎']
    msg = await ctx.send('Coin Flip!')
    for emoji in emojis:
        await msg.add_reaction(emoji)
    def check(reaction, user):
        if str(reaction.emoji) == '👍' : 
            return user == ctx.author and str(reaction.emoji) == '👍'
        if str(reaction.emoji) == '👎' :
            return user == ctx.author and str(reaction.emoji) == '👎'
    
    try:
        reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
    except asyncio.TimeoutError:
        if emojis[int((a*10) % 2)] == '👎':
            await ctx.send('nice')
        else:
            await ctx.send('not nice')
    else:
        if emojis[int((a*10) % 2)] == '👍':
            await ctx.send('nice')
        else:
            await ctx.send('not nice')

@client.command()
async def startbet(ctx, *, nameofbet):
    channel = ctx.message.channel
    emb = discord.Embed(
        title = 'Title', 
        description = 'This is a description', 
        colour = discord.Colour.blue()
        )
    emb.set_footer(text='This is a footer')
    emb.set_image(url='https://cdn.discordapp.com/attachments/412061704759934987/922281923840213002/5315.png')
    emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/412061704759934987/922281923840213002/5315.png')
    emb.set_author(name = 'Author name', icon_url = 'https://cdn.discordapp.com/attachments/412061704759934987/922281923840213002/5315.png')
    emb.add_field(name = 'Field Name', value = 'Field Value', inline = True)
    await ctx.send(embed=emb)
    await client.send_message(channel, embed=emb)
    
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
        else:
            #search for the video on youtube
            query_string = urllib.parse.urlencode({"search_query" : arg})
            html = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            url = video_ids[0]
        
        player = await YTDLSource.from_url(url, stream=True)
        vc.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

@client.command()
async def stop(ctx):
    await ctx.voice_client.disconnect()

client.run(os.getenv('DISCORD_TOKEN'))