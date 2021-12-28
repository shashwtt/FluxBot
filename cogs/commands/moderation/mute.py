import discord
import hex_colors

from discord.ext import commands
from discord.ext.commands import CommandOnCooldown, BucketType
from asyncio import sleep

colors = hex_colors.colors


class MuteUnmute(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='mute', aliases=['stfu'], help='Mute people (Mode is `s`, `m`, `h` or `d`)')
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, time: int=0, mode='m', *, reason="No reason provided"):
        role = discord.utils.get(ctx.guild.roles, name='Muted')  # Searching if the role already exists (If some other
        # bot made it)
        permissions = discord.Permissions(send_messages=False)  # Permission for new role (in case role doesn't exist)

        if not role in ctx.guild.roles:
            await ctx.send(
                "Hold on, making a 'Muted' role. Don't worry, this process won't take place every time you run this "
                "command")
            await ctx.guild.create_role(name='Muted', permissions=permissions,
                                        reason='For mute command')  # Making new role

        role = discord.utils.get(ctx.guild.roles, name='Muted')  # The old role variable might have returned None

        if role in member.roles:
            await ctx.send(f"{member} is already muted")
            return

        try:
            await member.add_roles(role, reason=f"{ctx.author} ran the mute command")
        except:
            await ctx.send(
                "The 'Muted' role is above my highest role. Please fix that in the server settings and then run the "
                "mute command. Having trouble doing that? Then simply deleted the 'Muted' role.")
            return

        em = discord.Embed(
            title=f"{ctx.author} muted {member}",
            description=f"Reason:\n{reason}",
            color=hex_colors.m_red
        )
        em.set_thumbnail(url=member.avatar_url)

        await ctx.send(embed=em)

        for channel in ctx.guild.channels:  # Changing the permission for the Muted role in all channels
            try:
                overwrite = channel.overwrites_for(role)
                overwrite.send_messages = False

                await channel.set_permissions(role, overwrite=overwrite)
            except:
                await ctx.send(
                    "Since I don't have the manage channels permission, I couldn't change the permissions for the "
                    "muted role in the channels.")
                break

        multiplier = 1

        if mode == 's' or mode == 'seconds' or mode == 'second':
            multiplier = 1
        if mode == 'm' or mode == 'minutes' or mode == 'minute':
            multiplier = 60
        if mode == 'h' or mode == 'hours' or mode == 'hour':
            multiplier = 60 * 60
        if mode == 'd' or mode == 'days' or mode == 'day':
            multiplier = 60 * 60 * 24

        await sleep(time * multiplier)
        if time != 0:
            await member.remove_roles(role, reason=f"Temporary mute is over. Responsible moderator: {ctx.author}")

    @commands.command(name='unmute', aliases=['unstfu'], help='Unmute muted people')
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, *, reason="No reason provided"):
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        if role is None:
            permissions = discord.Permissions(send_messages=False)
            await ctx.send(f"Your server doesn't have a 'Muted' role, I highly doubt {member} is muted")
            await ctx.guild.create_role(name='Muted', permissions=permissions,
                                        reason='For mute command')  # Making new role

            for channel in ctx.guild.channels:  # Changing the permission for the Muted role in all channels
                try:
                    overwrite = channel.overwrites_for(role)
                    overwrite.send_messages = False

                    await channel.set_permissions(role, overwrite=overwrite)
                except:
                    break

        if role not in member.roles:
            await ctx.send(f"{member} isn't even muted")
            return

        else:
            await member.remove_roles(role, reason=f'Unmute command ran by {ctx.author}')

            em = discord.Embed(
                title=f"{ctx.author} unmuted {member}",
                description=f"Reason:\n{reason}",
                color=hex_colors.l_green
            )
            em.set_thumbnail(url=member.avatar_url)

            await ctx.message.delete()
            await ctx.send(embed=em)


def setup(client):
    client.add_cog(MuteUnmute(client))
