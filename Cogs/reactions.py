import discord
from discord.ext import commands


class Reactions(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


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

            elif reaction.emoji == "U\1F5D1000": # FIXME: Currently broken on windows 8.1 as it does not recoginse this emoji
                await reaction.message.delete()
    
    @commands.Cog.listener()
    @commands.bot_has_permissions(manage_messages=True)
    async def on_reaction_clear_emoji(self, reaction:discord.Reaction):
            if reaction.emoji == "📌" and reaction.message.pinned == True: # TODO: Put pin emoji here
                await reaction.message.unpin(reason=f"Message unpinned due to all pin emojis removed")   


def setup(bot:commands.Bot):
    bot.add_cog(Reactions(bot))