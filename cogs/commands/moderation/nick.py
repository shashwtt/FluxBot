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
                description="A nickname cannot be longer than 32 digits...",
                colour=discord.Colour.brand_red()
            )
            embed_err.set_footer(text="Choose a shorter nickname!")
            await ctx.message.reply(embed=embed_err)
            return

        await user.edit(nick=nickname)
        embed = discord.Embed(
            description=f"{user.name}'s nickname was changed by {ctx.author.mention}!",
            colour=discord.Colour.yellow()
        )
        embed.add_field(name="nickname before -", value=f"```{user.nick}```", inline=True)
        embed.add_field(name="nickname now -", value=f"```{nickname}```", inline=True)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Nick(client))
