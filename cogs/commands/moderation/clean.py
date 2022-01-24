import discord

from discord.ext import commands
from discord.ext.commands import CommandOnCooldown, BucketType
import hex_colors

colors = hex_colors.colors

class Clean(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name='clean',
        aliases=['botdel', 'delbot'],
        help="Delete a lot of bot messages",
        description="Delete last 100 messages sent by an BOT account.. It will not delete the messages which are sent by actual users.. if you want to delete all messages look at delete command"
    )
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clean(self, ctx):
        def is_bot(m):
            return m.author.bot == True

        await ctx.channel.purge(limit=100, check=is_bot)
        await ctx.send(f"Deleted a lot of bot messages, {ctx.author.mention}")

def setup(client):
    client.add_cog(Clean(client))