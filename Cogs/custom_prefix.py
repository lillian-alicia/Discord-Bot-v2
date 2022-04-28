import discord, json
from discord.ext import commands
from json.decoder import JSONDecodeError


class custom_prefix(commands.Cog): # Setup bot
    def __init__ (self, bot):
        self.bot = bot
    
    class ConfigError(Exception):
        '''Error in provided config file.'''
        # TODO: Log errors in config file @logging

    try:
        global config
        config = json.load(open('Cogs/config.json', 'r')) # Load config file, and report error if necessary
    except JSONDecodeError as exception:
        config_error = bool(True)
        raise ConfigError('Unable to parse config file')

    global default_prefix
    try:
        if config['custom_prefix']['default'] == '':
            default_prefix = '!'
        else:
            default_prefix = str(config['custom_prefix']['default'])
    except:
        default_prefix = '!'


    @commands.command() # Change custom prefix
    async def change_prefix(self, ctx, custom_prefix):
        if bool(config['custom_prefix']['enable']) == True:
            with open('Media/prefixes.json', 'r') as prefix_file:
                prefixes = json.load(prefix_file) # Open prefix file

            prefixes[str(ctx.guild.id)] = custom_prefix

            with open ('Media/prefixes.json', 'w') as prefix_file: 
                json.dump(prefixes, prefix_file, indent=4) # Write changed prefix to file
            await ctx.send(f'Changed prefix to "{custom_prefix}"')
    
    @commands.Cog.listener()
    async def on_guild_join(guild): # Default prefix = ' ! '
        with open('Media/prefixes.json', 'r') as prefix_file:
            prefixes = json.load(prefix_file) # When the bot joins a server, save the default prefix in the
        prefixes[str(guild.id)] = default_prefix      # prefixes.json file

        with open ('Media/prefixes.json', 'w') as prefix_file:
            json.dump(prefixes, prefix_file, indent=4)


    @commands.Cog.listener() # Remove old servers from prefix file
    async def on_guild_remove(guild):
        with open('Media/prefixes.json', 'r') as prefix_file:
            prefixes = json.load(prefix_file) # When leaving a server, remove its prefix from the file
        prefixes.pop(str(guild.id))

        with open ('Media/prefixes.json', 'w') as prefix_file:
            json.dump(prefixes, prefix_file, indent=4)


         
def setup(bot):
    bot.add_cog(custom_prefix(bot))
