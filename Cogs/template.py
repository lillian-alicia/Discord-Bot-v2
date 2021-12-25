from json.decoder import JSONDecodeError
import discord, json
from discord.ext import commands

class template(commands.Cog): # Setup bot (replace template with suitable name)
    def __init__ (self, bot):
        self.bot = bot
    class ConfigError(Exception):
        '''Error in provided config file.'''
        # TODO: Log errors in config file @logging

    try:
        config = json.load(open('Cogs/config.json', 'r')) # Load config file, and report error if necessary
    except JSONDecodeError as exception:
        config_error = bool(True)
        raise ConfigError('Unable to parse config file')

    #
    # Commands and events go here. Commands are labeled '@commands.command()'
    # Events are labeled '@commands.Cog.listener()
    #
    #

def setup(bot):
    bot.add_cog(template(bot))
