import discord
import heroku3

from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, Cog


class Logs(Cog):
    def __init__(self, client):
        self.client = client

    @commands.is_owner()
    @commands.command(name="botlog", aliases=["heroku-log"])
    async def say(self, ctx, *, args):
        if ctx.message.author.id in self.client.owner_ids:
            await ctx.send(args)
        else:
            return

def setup(client):
    client.add_cog(Logs(client))
