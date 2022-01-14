import random
import sys

import discord
import requests

import hex_colors

from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, Cog


class Reboot(Cog):
    def __init__(self, client):
        self.client = client

    @commands.is_owner()
    @commands.command(name="reboot", aliases=['restart'], help="Stops the bot and starts it again...")
    async def shutdown(self, ctx):
        """
        Make the bot shutdown
        """
        if ctx.message.author.id in self.client.owner_ids:
            embed = discord.Embed(
                description="Restarting the bot! This may take a few seconds....",
                color=0x42F56C
            )
            await ctx.send(embed=embed)
            await self.bot.close()
        else:
            return


def setup(client):
    client.add_cog(Reboot(client))
