import os
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient

client = commands.Bot(command_prefix = '$')

# find a way to make it so that this doesnt need to be in the repo lol
TOKEN = "ODE2ODk5OTQ1MjEzODUzNzU2.YEBrXA.l6cSmHJYrzaLM5TQCUJCWt1hDrQ"

@client.command()
async def join(ctx):
    author = ctx.message.author
    channel = author.voice.channel
    await channel.connect()

client.run(TOKEN)