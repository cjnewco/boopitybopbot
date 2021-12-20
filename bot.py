import os
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient

#intents = discord.Intents.default()
#intents.members = True
client = commands.Bot(command_prefix = '$') #add intents=intents when ready

# find a way to make it so that this doesnt need to be in the repo lol
TOKEN = "ODE2ODk5OTQ1MjEzODUzNzU2.YEBrXA.l6cSmHJYrzaLM5TQCUJCWt1hDrQ"

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    #update server list in csv here
    #guild = await client.get_guild('Volskaya Industries')
    #for member in guild.members:
    #    print(member)

@client.command()
async def meow(ctx):
    author = ctx.message.author
    channel = author.voice.channel
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio('meow.mp3'), after=lambda e: print('done', e))
    
@client.command() 
async def startgamba(ctx, *, nameofgamba):
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


client.run(TOKEN)