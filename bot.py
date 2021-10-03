import discord, nest_asyncio, requests
from discord.ext import commands, tasks
import linecache as lc
import os, json, random

global root_dir
root_dir = 'home'
global default_prefix
default_prefix = '!'

# os.chdir('C:\Users\R-J\OneDrive\Documents\Discord-Bot\Discord-Bot-v2')

def get_prefix(client, message): # Per server prefixes
    with open('C:/Users/R-J/OneDrive/Documents/Discord-Bot/Discord-Bot-v2/Media/prefixes.json', 'r') as prefix_file:
        prefixes = json.load(prefix_file)
    return prefixes[str(message.guild.id)]


def random_status():
        for line in open('C:/Users/R-J/OneDrive/Documents/Discord-Bot/Discord-Bot-v2/Media/random_status.txt', 'r').readlines():
            status_options = []
            status_options.append (str(line))
        chosen_status = random.choice(status_options)
        return chosen_status

bot = commands.Bot(command_prefix = get_prefix) #create bot
nest_asyncio.apply() # Prevents program not starting due to asyncio
# bot.load_extension('Cogs.greetings')# Put the cog name here
# bot.load_extension('Cogs.eightball')

@bot.event
async def on_ready():
     chosen_status = random_status()
     await bot.change_presence(status=discord.Status.online)
     await bot.change_presence(activity=discord.Game(chosen_status))
     print('Bot is Online!')

@bot.event
async def on_member_join(ctx, member : discord.Member):
    if ctx.system_channel:
        await ctx.system_channel.send(f'{member.display_name}#{member.discriminator} has joined. Welcome!')

@bot.event
async def on_guild_join(guild): # Default prefix = ' ! '
     with open('C:/Users/R-J/OneDrive/Documents/Discord-Bot/Discord-Bot-v2/Media/prefixes.json', 'r') as prefix_file:
         prefixes = json.load(prefix_file) # When the bot joins a server, save the default prefix in the
     prefixes[str(guild.id)] = '!'      # prefixes.json file

     with open ('C:/Users/R-J/OneDrive/Documents/Discord-Bot/Discord-Bot-v2/Media/prefixes.json', 'w') as prefix_file:
         json.dump(prefixes, prefix_file, indent=4)

@bot.event
async def on_guild_remove(guild):
    with open('C:/Users/R-J/OneDrive/Documents/Discord-Bot/Discord-Bot-v2/Media/prefixes.json', 'r') as prefix_file:
        prefixes = json.load(prefix_file) # When leaving a server, remove it's prefix from the file
    prefixes.pop(str(guild.id))

    with open ('C:/Users/R-J/OneDrive/Documents/Discord-Bot/Discord-Bot-v2/Media/prefixes.json', 'w') as prefix_file:
        json.dump(prefixes, prefix_file, indent=4)

@bot.command
async def ping(ctx):
    bot_ping = (str(round(bot.latency * 1000)) + str(' ms'))
    await ctx.send(bot_ping)

@bot.command()
async def change_prefix(ctx, custom_prefix):
     with open('C:/Users/R-J/OneDrive/Documents/Discord-Bot/Discord-Bot-v2/Media/prefixes.json', 'r') as prefix_file:
         prefixes = json.load(prefix_file) # Save the custom prefix to the .json file
     prefixes[str(ctx.guild.id)] = custom_prefix

     with open ('C:/Users/R-J/OneDrive/Documents/Discord-Bot/Discord-Bot-v2/Media/prefixes.json', 'w') as prefix_file:
         json.dump(prefixes, prefix_file, indent=4)


bot.run(lc.getline('C:/Users/R-J/OneDrive/Documents/Discord-Bot/Discord-Bot-v2/Media/token', 1))
