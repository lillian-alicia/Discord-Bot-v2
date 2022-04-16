from json.decoder import JSONDecodeError
import discord, json
from discord.ext import commands
import logging
from datetime import datetime

global logger_commands
class logger(commands.Cog): # Setup bot (replace template with suitable name)
    def __init__ (self, bot):
        self.bot = bot
    class ConfigError(Exception):
        '''Error in provided config file.'''

    try:
        config = json.load(open('Cogs/config.json', 'r')) # Load config file, and report error if necessary
    except JSONDecodeError as exception:
        config_error = bool(True)
        raise ConfigError('Unable to parse config file')

    logger_commands = logging.getLogger('client') # Create logger for custom messages
    logger_commands.setLevel(logging.INFO)
    handler_commands = logging.FileHandler(filename='commands.log', encoding='utf-8', mode='w')
    handler_commands.setFormatter(logging.Formatter('%(levelname)s %(asctime)s - %(message)s', datefmt='%d-%b-%Y %H:%M:%S'))
    logger_commands.addHandler(handler_commands)
    

    @commands.Cog.listener()
    async def on_command(self, ctx):
        print("Command has been used.")
        source = f"{discord.Guild.name(ctx.guild)} #{ctx.channel}"
        command = ctx.command
        timestamp = str(datetime.datetime.now().strftime('%d-%m-%y-%H:%M'))
        logger_commands.info(f"{timestamp} - {command} used by {ctx.author} in {source}")

def setup(bot):
        logger_commands.info("----- Command Logging Enabled -----\n\n")
        bot.add_cog(logger(bot))
