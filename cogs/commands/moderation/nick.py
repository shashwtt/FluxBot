import discord
import hex_colors
import json

from db import *
from discord.ext import commands


class Nick(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='nick', aliases=['nickname', 'name'],
                      help='Manage server nickname..')
    @commands.bot_has_permissions(manage_nicknames=True)
    async def nick(self, ctx, user: discord.Member, *, nickname):
        if not ctx.author.guild_permissions.manage_nicknames and ctx.author != user:
            return

        if len(nickname) > 32:
            embed_err = discord.Embed(
                description="A nickname cannot be longer than 32 digits...\n\nChoose a shorter nickname!",
                colour=discord.Colour.yellow()
            )
            await ctx.send(embed=embed_err)
            return

        new_user = await user.edit(nick=nickname)
        embed = discord.Embed(
            description=f"{user.mention}'s nickname was changed by {ctx.author.mention}!",
            colour=discord.Colour.brand_green()
        )
        embed.add_field(name="nickname before -", value=user.nick)
        embed.add_field(name="nickname now -", value=new_user.nick)
        await ctx.send()

def setup(client):
    client.add_cog(Nick(client))
