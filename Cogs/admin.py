import discord 
from discord.ext import commands
import json

class Admin(commands.Cog): # Setup bot
    global config
    config = json.load(open('Cogs/config.json', 'r'))
    def __init__ (self, bot):
        self.bot = bot    
    
    @commands.command() # Change custom prefix
    async def change_prefix(self, ctx, custom_prefix):
        with open('Media/prefixes.json', 'r') as prefix_file:
            prefixes = json.load(prefix_file) # Open prefix file
    
        prefixes[str(ctx.guild.id)] = custom_prefix
     
        with open ('Media/prefixes.json', 'w') as prefix_file: 
            json.dump(prefixes, prefix_file, indent=4) # Write changed prefix to file
        await ctx.send(f'Changed prefix to "{custom_prefix}"')
         
    
    @commands.command()
    async def invite (self, ctx):
        permissions_int = str(config['permissions']) # Invite bot with permissions in config file
        invite_link = 'https://discord.com/api/oauth2/authorize?client_id=811660589037650000&permissions={premissions_int}&scope=bot'
        await ctx.send(f'Invite me using: {invite_link}') # TODO: Allow disable invite command in config file

#@commands.Cog.listener() '''  Auto-pin message, currently broken ''' FIXME
#async def on_reaction_add(self, ctx, reaction, user):
#    print (reaction.emoji)
#    await bot.pin_message(reaction.message)
#    if reaction.emoji == '📌':
#        print('Pin Message')
#        await ctx.pin_message(reaction.message)
    

    

def setup(bot):
    bot.add_cog(Admin(bot))
