import discord

from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, Cog


def bool_str(variable):  # Function to convert boolean values to string: Yes/No
    if variable == True:
        return 'Yes'
    if variable == False:
        return 'No'


class RoleInfo(Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name='roleinfo',
        aliases=['ri'],
        help='Shows information about a role')
    @cooldown(1, 10, BucketType.user)
    async def role_info(self, ctx, role: discord.Role):
        if role not in ctx.guild.roles:
            await ctx.send("I can't find that role in this server..")
            return

        perms = role.permissions  # returns a list of permissions

        d_perms = ''  # d stands for decorated

        for perm in perms:  # Rewriting the perms in a more presentable manner
            if not False in perm:  # We only want to log the permissions that the role has
                perm = str(perm)
                if '_' in perm:
                    perm = perm.replace('_', ' ')
                if 'guild' in perm:
                    perm = perm.replace('guild', 'server')  # Since guilds are called servers in the GUI
                if '(' in perm:
                    perm = perm.replace("('", '')
                    perm = perm.replace("'", '')
                    perm = perm.replace(')', '')
                    perm = perm.replace(',', ' ')

                perm = perm.title()  # Capitalizing first letter of every word
                perm = perm.replace('True', '')
                d_perms += f"`{perm}`"

        em = discord.Embed(title='@' + role.name,
                           color=role.color)  # I chose role.color, but that's a personal preference
        em.add_field(name='ID', value=role.id, inline=False)
        em.add_field(name="Permissions", value=d_perms, inline=False)
        em.add_field(name='Number of people that have this role', value=len(role.members), inline=False)
        em.add_field(name='Can everyone mention this role?', value=bool_str(role.mentionable), inline=False)

        await ctx.send(embed=em)


def setup(client):
    client.add_cog(RoleInfo(client))
