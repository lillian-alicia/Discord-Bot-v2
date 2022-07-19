import discord, re
from discord.ext import commands
from json import JSONDecodeError, load

# Variables
message_record = [] # A list of messages the we have responded to in the past 2 mins


class Reactions(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    
    class ConfigError(Exception):
        '''Error in provided config file.'''

    try:
        config = load(open('Cogs/config.json', 'r')) # Load config file, and report error if necessary
        global BOT_NAME
        BOT_NAME = config["settings"]["bot_name"]
    except JSONDecodeError as exception:
        config_error = bool(True)
        raise ConfigError('Unable to parse config file')

    @commands.Cog.listener()
    @commands.bot_has_permissions(manage_messages=True)

    async def on_reaction_add(self, reaction:discord.Reaction, user:discord.Member|discord.User):
        if discord.ext.commands.has_permissions(manage_messages = True): # If user can pin and delete messages:
            if reaction.emoji == "📌":
                try:
                    await reaction.message.pin(reason=f"Message pinned by {user.name}#{user.discriminator}")
                    await reaction.message.reply(f"Message pinned by {user.mention}")
                except discord.Forbidden:
                    await reaction.message.reply("Something went wrong. Do I have the `manage_messages` permission?")

            elif reaction.emoji == "🗑️":
                await reaction.message.delete()
    
    @commands.Cog.listener()
    @commands.bot_has_permissions(manage_messages=True)
    async def on_reaction_clear_emoji(self, reaction:discord.Reaction):
            if reaction.emoji == "📌" and reaction.message.pinned == True:
                await reaction.message.unpin(reason=f"Message unpinned due to all pin emojis removed")   


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction:discord.Reaction, user:discord.Member|discord.User):
        if reaction.emoji == "🔁":
            if reaction.message.content.isalnum(): # Check that the message has a number in it
                value = re.search(r'\d+', reaction.message.content) # Find number in message
                
                if value < 45: # Assume F
                    temp = (int(value) * 1.8) + 32
                    unit = "celsius"
                    unit_conv = "fahrenheit"
                
                else: # Assume C
                    temp = (int(value) - 32) / 1.8
                    unit = "fahrenheit"
                    unit_conv = "celsius"
                
                

                embed=discord.Embed(title="Temperature Conversion", color=0xff0000)
                embed.add_field(value=f"{value}° {unit} is {temp}° {unit_conv}", inline=False)
                embed.add_field(value=f"Conversion requested by {user.name}#{user.discriminator}")
                embed.set_author(name=BOT_NAME, icon_url="https://cdn.discordapp.com/avatars/811660589037650000/1e8e090bca1c50f583c7f810536366e3.png?size=256")

                await reaction.message.reply(embed=embed)
    
def setup(bot:commands.Bot):
    bot.add_cog(Reactions(bot))
