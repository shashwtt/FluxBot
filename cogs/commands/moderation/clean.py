import discord

from discord.ext import commands
from discord.ext.commands import CommandOnCooldown, BucketType
import hex_colors

colors = hex_colors.colors

class Clean(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='clean', help="Delete a lot of bot messages")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clean(self, ctx):
        def is_bot(m):
            return m.author.bot == True

        await ctx.channel.purge(limit=100, check=is_bot)
        await ctx.send(f"Deleted a lot of bot messages, {ctx.author.mention}")

def setup(client):
    client.add_cog(Clean(client))