import discord 
from discord.ext import commands

class Utility(commands.Cog): # Setup bot
    def __init__ (self, bot):
        self.bot = bot
    
    #
    # Commands and events go here. Commands are labeled '@commands.command()'
    # Events are labeled '@commands.Cog.listener()
    #
    #

def setup(bot):
    bot.add_cog(Utility(bot))
