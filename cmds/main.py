import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os
import json
from core.classes import Cog_Extension

with open('setting.json','r',encoding='utf8') as jfile:
    jdata=json.load(jfile)

class Main(Cog_Extension):
  
    @commands.command()
    async def ping(self,ctx):
        await ctx.send(f'{round(self.bot.latency*1000)}(ms)')

    @commands.command()
    async def say(self,ctx,*,msg):
        await ctx.send(msg)

    @commands.command(pass_context = True , aliases=jdata["clean"])
    async def clean(self,ctx,num:int):
        await ctx.channel.purge(limit=num+1)

    @commands.command()
    async def off(self,ctx):
        print('>> Shutdown Bot <<')
        os.remove("song.mp3")
        await self.bot.close()
    
    @commands.command(pass_conntext=True, aliases=jdata["play"])
    async def play(self,ctx,url:str):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients,guild=ctx.guild)
        if voice and voice.is_connected():
            song_there = os.path.isfile("song.mp3")
            try:
                if song_there:
                    os.remove("song.mp3")
                    print('Remove old song file')
            except PermissionError:
                print("Trying to delete song file, bot it's beingplayed")
                await ctx.send('ERROR: Music playing')
                return

            await ctx.send('Getting everything ready now')

            voice = get(self.bot.voice_clients,guild=ctx.guild)

            ydl_opts = {
                'format':'bestaudio/best',
                'quiet':True,
                'postprocessors':[{
                    'key':'FFmpegExtractAudio',
                    'preferredcodec':'mp3',
                    'preferredquality':'192',
                }],
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print('Downloadint audio now\n')
                ydl.download({url})
            
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    name = file
                    print(f'Renmed File:{file}\n')
                    os.rename(file,"song.mp3")

            voice.play(discord.FFmpegPCMAudio("song.mp3"),after=lambda e: print(f'{name} has finished playing'))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume=0.7

            nname=name.rsplit("-",2)
            await ctx.send(f'Playing:{nname}')
            print('playing\n')
        else:
            print('Bot不在語音頻道')
            await ctx.send("我不在任何語音頻道裡")
        
    @commands.command(pass_conntext=True)
    async def stop(self,ctx):
        voice = get(self.bot.voice_clients,guild=ctx.guild)
        
        if voice and voice.is_playing():
            print('Music stopped')
            os.remove("song.mp3")
            voice.stop()
            await ctx.send('Music stopped')
        else:
            print('Music not playing failed to stop')
            await ctx.send('音樂無法停止')

def setup(bot):
    bot.add_cog(Main(bot))

#@todo 暫停
#@todo 恢復