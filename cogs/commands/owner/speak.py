import random

import discord
import requests

import hex_colors

from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, Cog


class Speak(Cog):
    def __init__(self, client):
        self.client = client

    @commands.is_owner()
    @commands.command(name="speak", aliases=["echo"], help="Send a normal message via the bot...")
    async def say(self, ctx, *, args):
        if ctx.message.author.id in self.client.owner_ids:
            await ctx.send(args)
        else:
            return


def setup(client):
    client.add_cog(Speak(client))
