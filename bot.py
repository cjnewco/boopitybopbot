import os
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = '$', intents=intents)

# find a way to make it so that this doesnt need to be in the repo lol
TOKEN = "ODE2ODk5OTQ1MjEzODUzNzU2.YEBrXA.l6cSmHJYrzaLM5TQCUJCWt1hDrQ"

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    #update server list in csv here
    guild = await client.fetch_guild('Volskaya Industries')
    for member in guild.members:
        print(member)

@client.command()
async def meow(ctx):
    author = ctx.message.author
    channel = author.voice.channel
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio('meow.mp3'), after=lambda e: print('done', e))
    
@client.command() 
async def startgamba(ctx, *, nameofbet):
    emojis = ['👍','👎']
    msg = await ctx.send(nameofbet)
    for emoji in emojis:
        await msg.add_reaction(emoji)

@client.command()
async def play( ctx, *, arg ):
    if arg.startswith("http"):
        url = arg
        await ctx.send(arg)
    else:
        #search for the video on youtube
        print("lol you fucked up")

@client.command()
async def startbet(ctx, *, nameofbet):
    msg = await ctx.send(nameofbet)
    


client.run(TOKEN)