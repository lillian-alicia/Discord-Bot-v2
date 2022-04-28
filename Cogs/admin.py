import discord, json
from discord.ext import commands
from json.decoder import JSONDecodeError

class Admin(commands.Cog): # Setup bot
    global config
    config = json.load(open('Cogs/config.json', 'r'))
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



    
    @commands.command()
    async def invite (self, ctx):
        if bool(config['invite']['enable']) == True:
            permissions_int = str(config['invite']['permissions']) # Invite bot with permissions in config file
            invite_link = 'https://discord.com/api/oauth2/authorize?client_id=811660589037650000&permissions={premissions_int}&scope=bot'
            await ctx.send(f'Invite me using: {invite_link}') # TODO: Allow disable invite command in config file

def setup(bot):
    bot.add_cog(Admin(bot))
