# bot.py
import os
import discord
from discord.ext import commands 
client = commands.Bot(command_prefix = 'x')

TOKEN = 'ODE2ODk5OTQ1MjEzODUzNzU2.YEBrXA.l6cSmHJYrzaLM5TQCUJCWt1hDrQ'

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    if message.content.startswith('$yo'):
        await message.channel.send('hey bestie')

    if message.content.startswith('$kys'):
        await client.close()

client.run(TOKEN)