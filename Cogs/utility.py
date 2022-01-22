from os import name
import discord,json 
from discord.ext import commands
import json

from discord.guild import Guild

class Utility(commands.Cog): # Setup bot
    def __init__ (self, bot):
        self.bot = bot
    
    @commands.Cog.listener() # Welcome message
    async def on_member_join(self, ctx, member : discord.Member): #TODO: Editable welcome message in config file
        if ctx.system_channel:
            await ctx.system_channel.send(f'{member.display_name}#{member.discriminator} has joined. Welcome!')
            
    @commands.command()
    async def ping(self, ctx): # Client ping
        bot_ping = (str(round(self.bot.latency * 1000)) + str(' ms'))
        await ctx.send(bot_ping)

    @commands.command() # D&D weapon damage TODO: Test me
    async def damage(self, ctx, type, weapon):
        database = json.load(open('Media/DnD_weapons.json', 'r'))

        try:
            damage = database[type.lower()][weapon.lower()]
            await ctx.send(f'{weapon.capitalise()} deals {damage}')
        except:
            await ctx.send(f'No weapon called {weapon} in {type} weapons.')

    @commands.command()
    async def role(self, ctx, mode = '', role_name = '', *, data = ''):
        if mode.lower() == 'info':
            role_name = discord.utils.find(lambda m: m.name == role_name, ctx.guild.roles)
             
            if role_name == '':
                await ctx.send('No role found with that name.')

            role_id = Guild.get_role(role_name)
            await ctx.send(f'Role ID is {role_id}')
        elif mode.lower() == 'colour':
            '''change role colour - hex or rgb'''
        elif mode.lower() == 'members':
            '''Show members with certain role (embed)'''
        else:
            await ctx.send('role command options:\n info - show information about role \ncolour - change colour of a role \nmembers - show members with a role')


def setup(bot):
    bot.add_cog(Utility(bot))
