import random

import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, Cog

import hex_colors


def bool_str(variable):  # Function to convert boolean values to string: Yes/No
    if variable == True:
        return 'Yes'
    if variable == False:
        return 'No'


class ServerInfo(Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='serverinfo', help='Information about the server')
    @cooldown(1, 10, BucketType.guild)
    async def serverinfo(self, ctx):
        guild = server = ctx.guild

        # Many of these variables aren't necessary but since the embed has many fields, I didn't want the code to be messy
        created = server.created_at.strftime("%d %B %Y at %I %p")
        emojis = server.emojis
        members = server.member_count
        owner = server.owner
        level = server.verification_level
        boost_level = server.premium_tier
        large = server.large
        subs = server.premium_subscribers
        roles = len(ctx.guild.roles)

        em = discord.Embed(title=f"Here's the information I found on {ctx.guild.name}",
                           color=random.choice(hex_colors.colors))
        em.set_thumbnail(url=server.icon.url)
        em.add_field(name='ID', value=server.id, inline=False)
        em.add_field(name='Owner', value=owner, inline=False)
        em.add_field(name='Created on', value=created, inline=False)
        em.add_field(name='Is this server considered a big server?', value=bool_str(large), inline=False)
        em.add_field(name='Member Count', value=members)
        em.add_field(name='Number of roles', value=roles - 1, inline=False)  # To ignore @everyone role
        em.add_field(name='Emojis', value=len(emojis), inline=False)
        em.add_field(name='Security Level', value=str(level).capitalize(), inline=False)
        em.add_field(name='Server Boosters', value=len(subs), inline=False)
        em.add_field(name='Server level', value=boost_level, inline=False)
        em.set_footer(text=f'Requested by {ctx.author.display_name}', icon_url=ctx.author.avatar.url)

        await ctx.send(embed=em)


def setup(client):
    client.add_cog(ServerInfo(client))
