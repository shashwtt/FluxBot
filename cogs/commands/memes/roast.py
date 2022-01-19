import aiohttp
import discord
import requests

import hex_colors

from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, Cog


def bool_str(variable):  # Function to convert boolean values to string: Yes/No
    if variable:
        return 'Yes'
    if not variable:
        return 'No'


class Roast(Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name='roast',
        aliases=['insult'],
        help="Bully someone!!",
        brief="roast [user]")
    async def roast(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        if user.bot:
            await ctx.send("I'm not gonna roast someone of my own kind!")
            return

        url = 'https://insult.mattbas.org/api/en/insult.json'
        # Visit https://insult.matlabs.org/api/ for documentation
        response = requests.get(url, params={'who': user.mention}).json()
        await ctx.send(user.mention + response['insult'])


def setup(client):
    client.add_cog(Roast(client))
