import discord 
from discord.ext import commands
import json

class Utility(commands.Cog): # Setup bot
    def __init__ (self, bot):
        self.bot = bot
    
    @commands.Cog.listener() # Welcome message
    async def on_member_join(self, ctx, member : discord.Member):
        if ctx.system_channel:
            await ctx.system_channel.send(f'{member.display_name}#{member.discriminator} has joined. Welcome!')
            
    @commands.command()
    async def ping(self, ctx): # Client ping
        bot_ping = (str(round(self.bot.latency * 1000)) + str(' ms'))
        await ctx.send(bot_ping)

    @commands.command() # D&D weapon damage
    async def damage(self, ctx, type, weapon):
        database = json.load(open('Media/DnD_weapons.json', 'r'))

        try:
            damage = database[type.lower()][weapon.lower()]
            await ctx.send(f'{weapon.capitalise()} deals {damage}')
        except:
            await ctx.send(f'No weapon called {weapon} in {type} weapons.')


def setup(bot):
    bot.add_cog(Utility(bot))
