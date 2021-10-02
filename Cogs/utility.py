import discord 
from discord.ext import commands

class Utility(commands.Cog):
    def __init__ (self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, ctx, member : discord.Member):
        if ctx.system_channel:
            await ctx.system_channel.send(f'{member.display_name}#{member.discriminator} has joined. Welcome!')
            
    @commands.command()
    async def ping(self, ctx):
        bot_ping = (str(round(bot.latency * 1000)) + str(' ms'))
        await ctx.send(bot_ping)

def setup(bot):
    bot.add_cog(Utility(bot))
