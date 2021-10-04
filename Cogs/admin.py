import discord 
from discord.ext import commands
import json

class Admin(commands.Cog):
    def __init__ (self, bot):
        self.bot = bot
    
    @commands.command()
    async def change_prefix(self, ctx, custom_prefix):
        with open('Media/prefixes.json', 'r') as prefix_file:
            prefixes = json.load(prefix_file) # Save the custom prefix to the .json file
    
        prefixes[str(ctx.guild.id)] = custom_prefix
     
        with open ('Media/prefixes.json', 'w') as prefix_file: 
            json.dump(prefixes, prefix_file, indent=4) 
        await ctx.send(f'Changed prefix to "{custom_prefix}"')
         
    
    @commands.command()
    async def invite (self, ctx):
        invite_link = 'https://discord.com/api/oauth2/authorize?client_id=811660589037650000&permissions=926940919&scope=bot'
        await ctx.send(f'Invite me using: {invite_link}')

#@commands.Cog.listener()
#async def on_reaction_add(self, ctx, reaction, user):
#    print (reaction.emoji)
#    await bot.pin_message(reaction.message)
#    if reaction.emoji == '📌':
#        print('Pin Message')
#        await ctx.pin_message(reaction.message)
    

    

def setup(bot):
    bot.add_cog(Admin(bot))
