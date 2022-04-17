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
        colour_hex = ('%02x%02x%02x' % (role.colour.r, role.colour.g, role.colour.b))
        #colour_hex = role.colour.value
        creation_date = role.created_at
        members = role.members
        num_members = len(role.members)
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
            await ctx.reply("No colour given. Enter a colour, or type `random` for a random colour")

        elif discord.ext.commands.has_permissions(manage_roles=True):

                if colour.lower() == "random":
                    new_colour = discord.Colour.random()
                elif len(colour) == 6:
                    raw_colour = int(str(colour), 16)
                    new_colour = discord.Colour(raw_colour)
                else:
                    raw_colour = colour.split(" ")
                    r = int(raw_colour[0])
                    g = int(raw_colour[1])
                    b = int(raw_colour[2])

                    raw_colour_hex = ('%02x%02x%02x' % (r, g, b))
                    raw_colour = int(str(raw_colour_hex), 16)

                    new_colour = discord.Colour(raw_colour)
                    """convert from separate r,g,b inputs"""

                try: # Try to edit role
                    reason = f"Colour changed by {ctx.author.name}#{ctx.author.discriminator}"
                    await role.edit(colour = new_colour, reason=reason)
                    await ctx.reply(f"Sucessfully changed role colour to `{colour}`.")
                except discord.Forbidden:
                    await ctx.reply("Something went wrong. Do I have permission to edit this role?")

                
                """TODO: Implement HERE
                ~# 1 - Check for perms~
                # 2 - Convert colour to proper format (accept hex, or tuple (r,g,b))
                ~# 3 - Complain if no colour given~"""

        else:
            await ctx.reply ("{ctx.author.mention} You do not have the correct permissions to modify roles.")

    @commands.command(aliases=["permissions"])
    async def perms(self, ctx, role : discord.Role, mode=""):
        permissions = role.permissions
        embed=discord.Embed(title=f"Permissions for {role}", description=f"Info requested by {ctx.author}", color=role.colour)
        embed.set_author(name=f"{str(ctx.author.name)}#{str(ctx.author.discriminator)}")

        perms_int = permissions.value

        if mode.lower() == "voice":
            embed.add_field(name="Connect:", value=f"`{permissions.connect}`", inline=True)
            embed.add_field(name="Deafen Members:", value=f"`{permissions.deafen_members}`", inline=True)
            embed.add_field(name="Kick Members:", value=f"`{permissions.kick_members}`", inline=True)
            embed.add_field(name="Move Members:", value=f"`{permissions.move_members}`", inline=True)
            embed.add_field(name="Mute Members:", value=f"`{permissions.mute_members}`", inline=True)
            embed.add_field(name="Priority Speaker:", value=f"`{permissions.priority_speaker}`", inline=True)
            embed.add_field(name="Speak:", value=f"`{permissions.speak}`", inline=True)
            embed.add_field(name="Stream:", value=f"`{permissions.stream}`", inline=True)
            embed.add_field(name="Use Voice Activity:", value=f"`{permissions.use_voice_activation}`", inline=True)
            embed.add_field(name="Permissions Integer:", value=perms_int, inline=False)

        elif mode.lower() == "admin" or mode.lower() == "mod":
            embed.add_field(name="Administrator:", value=f"`{permissions.administrator}`", inline=True)
            embed.add_field(name="Manage Server:", value=f"`{permissions.manage_guild}`", inline=True)
            embed.add_field(name="Manage Channels:", value=f"`{permissions.manage_channels}`", inline=True)
            embed.add_field(name="Manage Roles:", value=f"`{permissions.manage_roles}`", inline=True)
            embed.add_field(name="Manage Messages:", value=f"`{permissions.manage_messages}`", inline=True)
            embed.add_field(name="Manage Nicknames:", value=f"`{permissions.manage_nicknames}`", inline=True)
            embed.add_field(name="Manage Emojis:", value=f"`{permissions.manage_emojis}`", inline=True)
            embed.add_field(name="Kick Members:", value=f"`{permissions.kick_members}`", inline=True)
            embed.add_field(name="Ban Members:", value=f"`{permissions.ban_members}`", inline=True)
            embed.add_field(name="Audit Log:", value=f"`{permissions.view_audit_log}`", inline=True)
            embed.add_field(name="Permissions Integer:", value=perms_int, inline=False)

        elif mode.lower == "text" or mode.lower() == "channels":
            embed.add_field(name="Add Reactions:", value=f"`{permissions.add_reactions}`", inline=True)
            embed.add_field(name="Attach Files:", value=f"`{permissions.attach_files}`", inline=True)
            embed.add_field(name="Change own Nickname:", value=f"`{permissions.change_nickname}`", inline=True)
            embed.add_field(name="Embed Links:", value=f"`{permissions.embed_links}`", inline=True)
            embed.add_field(name="Use External Emojis:", value=f"`{permissions.use_external_emojis}`", inline=True)
            embed.add_field(name="Mention @everyone:", value=f"`{permissions.mention_everyone}`", inline=True)
            embed.add_field(name="Message History:", value=f"`{permissions.read_message_history}`", inline=True)
            embed.add_field(name="Read Messages:", value=f"`{permissions.read_messages}`", inline=True)
            embed.add_field(name="Send Messages:", value=f"`{permissions.send_messages}`", inline=True)
            embed.add_field(name="Send TTS Messages:", value=f"`{permissions.send_tts_messages}`", inline=True)
            embed.add_field(name="View Channel:", value=f"`{permissions.view_channel}`", inline=True)
            embed.add_field(name="Permissions Integer:", value=perms_int, inline=False)
            
        else:
            with open('C:/Users/R-J/OneDrive/Documents/Discord-Bot/Discord-Bot-v2/Media/prefixes.json', 'r') as prefix_file:
                prefixes = json.load(prefix_file)

            server_prefix = f"{prefixes[str(ctx.guild.id)]}"
            embed.add_field(name="Invalid Input:", value=f"`{server_prefix}permissions *@role* *mode*`", inline=True)
            embed.add_field(name="Voice:", value="Voice channel related permissions", inline=True)
            embed.add_field(name="Text/Channels:", value="Text channel related permissions", inline=True)
            embed.add_field(name="Admin/Mod:", value="Administrator or Moderator related permissions", inline=True)

        await ctx.send(embed=embed)

    # Events are labeled '@commands.Cog.listener()
    #
    #

def setup(bot):
    bot.add_cog(roles(bot))