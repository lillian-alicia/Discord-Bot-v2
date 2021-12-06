import discord, nest_asyncio, requests
from discord.ext import commands, tasks
import linecache as lc
import os, json, random

config = json.load(open('Cogs/config.json', 'r'))

global default_prefix
default_prefix = '!'

def auth_owner(config, context):
    owner_username = config['owner']['username']
    owner_discriminator = config['owner']['discriminator']

    author_username = context.author.username
    author_discrim = context.author.discriminator

    if owner_username == author_username and owner_discriminator == author_discrim:
        owner = True
    else:
        owner = False
    return bool(owner)

def get_prefix(client, message): # Per server prefixes
    with open('C:/Users/R-J/OneDrive/Documents/Discord-Bot/Discord-Bot-v2/Media/prefixes.json', 'r') as prefix_file:
        prefixes = json.load(prefix_file)
    return prefixes[str(message.guild.id)]

def random_status(): # Random playing status from txt file
        for line in open('C:/Users/R-J/OneDrive/Documents/Discord-Bot/Discord-Bot-v2/Media/random_status.txt', 'r').readlines():
            status_options = []
            status_options.append (str(line))
        chosen_status = random.choice(status_options)
        return chosen_status

bot = commands.Bot(command_prefix = get_prefix) #create bot
nest_asyncio.apply() # Prevents program not starting due to asyncio

bot.load_extension('Cogs.admin')# Loading cogs
bot.load_extension('Cogs.utility')
bot.load_extension('Cogs.fun')

@bot.event
async def on_ready(): # Apply random status
     chosen_status = random_status()
     await bot.change_presence(status=discord.Status.online)
     await bot.change_presence(activity=discord.Game(chosen_status))
     print('Bot is Online!')

@bot.event
async def on_guild_join(guild): # Default prefix = ' ! '
     with open('C:/Users/R-J/OneDrive/Documents/Discord-Bot/Discord-Bot-v2/Media/prefixes.json', 'r') as prefix_file:
         prefixes = json.load(prefix_file) # When the bot joins a server, save the default prefix in the
     prefixes[str(guild.id)] = '!'      # prefixes.json file

     with open ('C:/Users/R-J/OneDrive/Documents/Discord-Bot/Discord-Bot-v2/Media/prefixes.json', 'w') as prefix_file:
         json.dump(prefixes, prefix_file, indent=4)


@bot.event # Remove old servers from prefix file
async def on_guild_remove(guild):
    with open('C:/Users/R-J/OneDrive/Documents/Discord-Bot/Discord-Bot-v2/Media/prefixes.json', 'r') as prefix_file:
        prefixes = json.load(prefix_file) # When leaving a server, remove its prefix from the file
    prefixes.pop(str(guild.id))

    with open ('C:/Users/R-J/OneDrive/Documents/Discord-Bot/Discord-Bot-v2/Media/prefixes.json', 'w') as prefix_file:
        json.dump(prefixes, prefix_file, indent=4)


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
        for i in range(0, len(config['cogs'])):
            cog_name = config['cogs'][i]
            try:
                bot.reload_extension(f'Cogs.{cog_name}')
            except:
                await ctx.send(f'Failed to restart {cog_name}.')
    else:
        print('Only the owner can use this command. If you are the owner, edit the values in config.json')


bot.run(lc.getline('C:/Users/R-J/OneDrive/Documents/Discord-Bot/Discord-Bot-v2/Media/token', 1))
