import discord
from discord.ext import commands


class Reactions(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    @commands.bot_has_permissions(perms=discord.Permissions.manage_messages)

    async def on_reaction_add(self, ctx, reaction:discord.Reaction, user:discord.Member|discord.User):
        if user.Permissions.manage_messages == True: # If user can pin and delete messages:
            if reaction.emoji == "": # TODO: Put pin emoji here
                await reaction.message.pin(reason=f"Message pinned by {user.name}#{user.discriminator}")

            elif reaction.emoji == "": # TODO: Put bin emoji here
                await reaction.message.delete()
    
    @commands.Cog.listener()
    @commands.bot_has_permissions(perms=discord.Permissions.manage_messages)
    async def on_reaction_clear_emoji(self, reaction:discord.Reaction):
            if reaction.emoji == "" and reaction.message.pinned == True: # TODO: Put pin emoji here
                await reaction.message.unpin(reason=f"Message unpinned due to all pin emojis removed")   


def setup(bot:commands.Bot):
    bot.add_cog(Reactions(bot))