import os
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient

client = commands.Bot(command_prefix = '$')

# find a way to make it so that this doesnt need to be in the repo lol
TOKEN = "ODE2ODk5OTQ1MjEzODUzNzU2.YEBrXA.l6cSmHJYrzaLM5TQCUJCWt1hDrQ"

@client.command()
async def meow(ctx):
    author = ctx.message.author
    channel = author.voice.channel
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio('meow.mp3'), after=lambda e: print('done', e))

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    
@client.command
async def startbet():
	global myList
	myList = []
	title = text[8:]
	message.channel.send(title)


client.run(TOKEN)