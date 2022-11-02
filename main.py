import discord
from discord.ext import commands
import os
import pytube as pt
from pathlib import Path

from apikeys import *

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix = '!', intents=intents)
players = {}
queue = []
queue_url = []

async def playsong(ctx):
    url = queue_url[0]
    print(f'url: {url}')
    yt = pt.YouTube(url)
    t = yt.streams.filter(only_audio=True)
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    path = Path(f"Downloads/{queue[0]}.mp4")
    print(path)

    print(queue)
    if path.is_file():
        print(queue)
        print(f"Found Song {queue[0]}")
        await ctx.send(f'**Now playing:** {queue[0]}')
        voice.play(discord.FFmpegPCMAudio(path), after=lambda x=None: playsong(ctx))
        queue.pop(0)
        queue_url.pop(0)
    else:
        ctx.send(f"**Playing:** {queue[0]}.")
        print(f"Downloading song {queue[0]}")
        await ctx.send(f'**Now playing:** {queue[0]}')
        voice.play(discord.FFmpegPCMAudio(t[0].download("Downloads")), after=lambda x=None: playsong(ctx))
        queue.pop(0)
        queue_url.pop(0)

@client.event
async def on_ready():
    print("The bot is ready!")
    print("------------------")

@client.command()
async def hello(ctx):
    await ctx.send("Hello")

@client.command()
async def join(ctx):
    if not ctx.message.author.voice:
            await ctx.send("You are not connected to a voice channel!")
            return
    else:
        channel = ctx.message.author.voice.channel
        await ctx.send(f'Connected to ``{channel}``')

    await channel.connect()

@client.command()
async def play(ctx, url : str):
    
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel!")
        return
    else:
        channel = ctx.message.author.voice.channel
        print(channel)
        print(ctx.voice_client)

        if not ctx.voice_client:
            print(channel)
            await channel.connect()    
            await ctx.send(f'Connected to ``{channel}``')
        
        elif ctx.voice_client.channel == channel:
            print("same channel")

        elif ctx.voice_client != channel:
            await ctx.send("Your in a diffrent voice channel to me")
            return

    yt = pt.YouTube(url)
    t = yt.streams.filter(only_audio=True)

    if ctx.voice_client.is_playing():
        print("playing")
        await ctx.send(f'**Added** {yt.title} **to the queue!**')
        queue.append(yt.title)
        queue_url.append(url)
        print(queue)
    else:
        queue.append(yt.title)
        queue_url.append(url)
        await playsong(ctx)

@client.command()
async def skip(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    print("stopped")
    voice.stop()
    await playsong(ctx)
    

@client.command()
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    user = ctx.message.author.mention
    await voice_client.disconnect()
    await ctx.send(f'Disconnected from {user}')


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()
    
client.run(BOTTOKEN)
