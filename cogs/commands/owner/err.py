import discord

from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, Cog


class Err(Cog):
    def __init__(self, client):
        self.client = client

    @commands.is_owner()
    @commands.command(name="err", help="Raise errors, wait whaa..")
    async def err(self, ctx, *, err_name):
        await ctx.reply('boobs')


def setup(client):
    client.add_cog(Err(client))
