import discord
import hex_colors
import json

from db import *
from discord.ext import commands


class Nick(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='nick', aliases=['nickname', 'name'],
                      help='Change someone\'s nickname on the server..')
    @commands.has_permissions(manage_nicknames=True)
    @commands.bot_has_permissions(manage_nicknames=True)
    async def nick(self, ctx, user: discord.Member, *, nickname):
        if len(nickname) > 32:
            embed_err = discord.Embed(
                description="A nickname cannot be longer than 32 digits...\n\nChoose a shorter nickname!",
                colour=discord.Colour.brand_red()
            )
            return

        try:
            await user.edit(nick=nickname)
        except Exception:
            print(Exception)



def setup(client):
    client.add_cog(Nick(client))
