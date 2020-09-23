import discord
import json
from discord.ext import commands
from core.classes import Cog_Extension

with open('setting.json','r',encoding='utf8') as jfile:
    jdata=json.load(jfile)

class Event(Cog_Extension):
    @commands.Cog.listener()
    async def on_member_join(self,mamber):
        channel=self.bot.get_channel(int(jdata['channel']))
        await channel.sand(f'{member} join~')

    @commands.Cog.listener()
    async def on_member_remove(self,mamber):
        channel=self.bot.get_channel(int(jdata['channel']))
        await channel.sand(f'{member} leave~')

def setup(bot):
    bot.add_cog(Event(bot))