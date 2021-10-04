import discord, random
from discord.ext import commands

class Utility(commands.Cog):
    def __init__ (self, bot):
        self.bot = bot
    
    @commands.command()
    async def random(self, ctx, mode, *, params):
        if mode == 'number':
            params_split = params.split()
            params_split = params_split.sort()

            if len(params_split) > 2 or len(params_split) < 2:
                await ctx.send('Please give two numbers.')
            
            random_result = random.randint(params_split[0], params_split [1])
            await ctx.send(f'Picked a random number between {params_split[0]} and {params_split[1]}. Result - {random_result}')
            
        elif mode == 'choice':
            params_split = params.split()

            if len(params_split) < 2:
                print('Please give at least two choices.')

            random_result = random.choice(params_split)
            await ctx.send(f'Picked  {random_result}.')
        
        else:
            await ctx.send('Available options for random: number, choice')


def setup(bot):
    bot.add_cog(Utility(bot))