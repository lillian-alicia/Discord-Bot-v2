from colorsys import rgb_to_hsv
from json.decoder import JSONDecodeError
import discord, json
from discord.ext import commands

class roles(commands.Cog): # Setup bot (replace template with suitable name)
    def __init__ (self, bot):
        self.bot = bot
    class ConfigError(Exception):
        '''Error in provided config file.'''
        # TODO: Log errors in config file @logging

    try:
        config = json.load(open('Cogs/config.json', 'r')) # Load config file, and report error if necessary
    except JSONDecodeError as exception:
        config_error = bool(True)
        raise ConfigError('Unable to parse config file')

    



    #
    @commands.command()
    async def info(self, ctx, role : discord.Role):
        
        # role hex colour, number of users with role, role name, creation date, permission integer
        colour = role.colour
        colour_hex = ('%02x%02x%02x' % (role.colour.r, role.colour.g, role.colour.b))
        #colour_hex = role.colour.value
        creation_date = role.created_at
        members = role.members
        num_members = len(role.members)
        print(role.members)
        permissions = role.permissions.value
        # TODO: Write subprogram to handle permissions objects

        def format_members(members):
            if num_members == 1:
                out_str = str(members[0].display_name)
                return out_str
            out_str = ""
            for member in members:
                out_str = out_str + f"{member.display_name}" + ", "
            return out_str[0:(len(out_str)-2)]
                

        embed=discord.Embed(title=f"Role info for {role}", description=f"Info requested by {ctx.author}", color=role.colour) # TODO: mention ctx.author FIXME: colour should not be given in str
        embed.set_author(name=f"{str(ctx.author.name)}#{str(ctx.author.discriminator)}")
        embed.add_field(name="Colour", value=f"{role.colour.r}, {role.colour.g}, {role.color.b}    #{colour_hex}", inline=True)
        embed.add_field(name="Creation Date", value=creation_date, inline=True)
        embed.add_field(name="Members:", value=format_members(members), inline=False)
        embed.add_field(name="Number of Members", value=num_members, inline=True)
        embed.add_field(name="Permissions Integer", value=permissions, inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(manage_roles=True)
    async def colour(self, ctx, role : discord.Role,*, colour):
        if colour == "":
            await ctx.reply("No colour given. Enter a colour, or type ```random``` for a random colour")

        elif ctx.author.permssions.manage_roles:

                if colour.lower() == "random":
                    new_colour = discord.Colour.random()
                try:
                    raw_colour = str(int(str(colour), 16))
                    new_colour = discord.Colour(raw_colour)
                except:
                    raw_colour = colour.split(" ")
                    r = int(raw_colour[0])
                    g = int(raw_colour[1])
                    b = int(raw_colour[2])

                    raw_colour = ('%02x%02x%02x' % (r, g, b))

                    new_colour = discord.Colour(raw_colour)
                    """convert from separate r,g,b inputs"""

                try: # Try to edit role
                    reason = f"Colour changed by {ctx.author.name}#{ctx.author.discriminator}"
                    await role.edit(colour = new_colour, reason=reason)
                    await ctx.reply(f"Sucessfully changed role colour to {colour}.")
                except discord.Forbidden:
                    await ctx.reply("Something went wrong. Do I have the `manage_messages` permission?")

                
                """TODO: Implement HERE
                ~# 1 - Check for perms~
                # 2 - Convert colour to proper format (accept hex, or tuple (r,g,b))
                ~# 3 - Complain if no colour given~"""

        else:
            await ctx.reply ("{ctx.author.mention} You do not have the correct permissions to modify roles.")



    # Events are labeled '@commands.Cog.listener()
    #
    #

def setup(bot):
    bot.add_cog(roles(bot))