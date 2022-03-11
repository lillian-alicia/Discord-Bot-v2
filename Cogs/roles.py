from json.decoder import JSONDecodeError
import discord, json
from discord.ext import commands

class roles(commands.Cog): # Setup bot (replace template with suitable name)
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
    @commands.command()
    async def info(role : discord.role):
        
        # role hex colour, number of users with role, role name, creation date, permission integer
        colour = discord.colour.to_rgb(role.colour) #(r, g, b)
        creation_date = role.created_at()
        members = role.members
        num_members = int(len(role.members))
        permissions = role.permissions #put something here to get perms int


    # Events are labeled '@commands.Cog.listener()
    #
    #

def setup(bot):
    bot.add_cog(roles(bot))