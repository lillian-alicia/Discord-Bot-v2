from json.decoder import JSONDecodeError
import discord, nest_asyncio, requests
from discord import channel #FIXME: Add improved error handling @logging
from discord.ext import commands, tasks
import linecache as lc
import os, json, random # Is os module required?
import logging #TODO: Add command logging (user, channel, server, time)

class ConfigError(Exception):
    '''Error in provided config file.'''
    # TODO: Log errors in config file @logging

try:
    config = json.load(open('Cogs/config.json', 'r')) # Load config file, and report error if necessary
except JSONDecodeError as exception:
    config_error = bool(True)
    raise ConfigError('Unable to parse config file')


global default_prefix
if config['custom_prefix']['default'] == '':
    default_prefix = '!'
else:
    default_prefix = str(config['custom_prefix']['default'])

def auth_owner(config, context): # Subprogram to authenticate owner as message author
    owner_username = config['owner']['username']
    owner_discriminator = config['owner']['discriminator']

    author_username = context.author.username
    author_discrim = context.author.discriminator
    
    try:
        if owner_username == author_username and owner_discriminator == author_discrim:
            owner = True
        else:
            owner = False
        return bool(owner)
    except:
        context.send('Error in configuration file. Unable to validate owner.')
        try:
            raise ConfigError('Error with owner details in config file')
            #TODO: Log error @logging
        except ConfigError as ex:
            print(ex)
        return bool(False)

def get_prefix(client, message): # Load Per server prefix
    if bool(config['custom_prefix']['enable']) == True:
        with open('C:/Users/R-J/OneDrive/Documents/Discord-Bot/Discord-Bot-v2/Media/prefixes.json', 'r') as prefix_file:
            prefixes = json.load(prefix_file)
        return prefixes[str(message.guild.id)]
    else:
        return default_prefix

def random_status(): # Random playing status from Media/random_status.txt file
        for line in open('C:/Users/R-J/OneDrive/Documents/Discord-Bot/Discord-Bot-v2/Media/random_status.txt', 'r').readlines():
            status_options = []
            status_options.append (str(line))
        chosen_status = random.choice(status_options)
        return chosen_status

bot = commands.Bot(command_prefix = get_prefix) #create bot
nest_asyncio.apply() # Prevents program not starting due to asyncio

bot.load_extension('Cogs.admin')# Loading cogs
bot.load_extension('Cogs.utility') # TODO: Only load cogs given in config file - possible error if cog does not exist
bot.load_extension('Cogs.fun')

@bot.event
async def on_ready(): # Apply random status from text file unless a specific status is set
    if config['settings']['status'] == '':
        chosen_status = random_status()
        
    else:
        chosen_status = config['settings']['status']
    await bot.change_presence(status=discord.Status.online)
    await bot.change_presence(activity=discord.Game(chosen_status))
    print('Bot is Online!')

@bot.command() # Enable chosen cogs
async def load_cog (ctx, cog_name):

    owner = bool(auth_owner(config, ctx))
    
    if owner == True:
        try:
            bot.load_extension(f'Cogs.{cog_name}')
            await ctx.send(f'Loaded {cog_name}!')
        except:
            await ctx.send(f'Failed to load {cog_name}.')
    else:
        print('Only the owner can use this command. If you are the owner, edit the values in config.json')

@bot.command() # Disable chosen cogs
async def unload_cog (ctx, cog_name):
      owner = bool(auth_owner(config, ctx))
      if owner == True:
        try:
            bot.unload_extension(f'Cogs.{cog_name}')
            await ctx.send(f'Unloaded {cog_name}!')
        except:
            await ctx.send(f'Failed to unload {cog_name}.')
      else:
          print('Only the owner can use this command. If you are the owner, edit the values in config.json')

@bot.command() # Reload all cogs - update code without restarting bot
async def reload (ctx):
    owner = bool(auth_owner(config, ctx))
    if owner == True:
        try:
            for i in range(0, len(config['settings']['cogs'])):
                cog_name = config['settings']['cogs'][i]
                try:
                    bot.reload_extension(f'Cogs.{cog_name}')
                except: # Failed to load specific cog
                    await ctx.send(f'Failed to restart {cog_name}.')
        except: # Failed to read config file
            try:
                raise ConfigError('Failed to find enabled cogs in config file.')
                #TODO: Log error @logging
            except ConfigError as ex:
                print(ex)

    else:
        await('Only the owner can use this command. If you are the owner, edit the values in config.json')

if str(config['settings']['token']) == '': # If there is no token in config file, use token file
    token = lc.getline('Media/token', 1)
else:
    try:
        token = str(config['settings']['token'])
    except:
        try:
            raise ConfigError('No token provided in config or token file.')
            #TODO: Log error @logging
        except ConfigError as ex:
            print(ex)

bot.run(token)