import discord
from discord.ext import commands
from discord.utils import get
import os
import asyncio
import json

with open('setting.json','r',encoding='utf8') as jfile:
    jdata=json.load(jfile)

bot=commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(">> Bot is online <<")

@bot.command()
async def load(ctx,extension):
    bot.load_extension(f'cmds.{extension}')
    await ctx.send(f'Loaded {extension}')

@bot.command()
async def unload(ctx,extension):
    bot.unload_extension(f'cmds.{extension}')
    await ctx.send(f'Unloaded {extension}')

@bot.command()
async def reload(ctx,extension):
    bot.reload_extension(f'cmds.{extension}')
    await ctx.send(f'Reloaded {extension}')

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    voice = get(bot.voice_clients,guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await ctx.send(f'加入 {channel}')

@bot.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients,guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        print(f'Bot已離開 {channel}')
        os.remove("song.mp3")
    else:
        print('Bot不在語音頻道')
        await ctx.send("我不在任何語音頻道裡")

for f in os.listdir('cmds'):
    if f.endswith('.py'):
        bot.load_extension(f'cmds.{f[:-3]}')

if __name__=="__main__":
    bot.run(jdata['TOKEN'])