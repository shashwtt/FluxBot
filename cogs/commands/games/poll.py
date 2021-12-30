import random

import discord
import requests

import hex_colors

from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, Cog


class Poll(Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="poll", aliases=["vote"])
    async def poll(self, context, *, title):
        """
        Create a poll where members can vote.
        """
        embed = discord.Embed(
            title="A new poll has been created!",
            description=f"{title}",
            color=0x42F56C
        )
        embed.set_footer(
            text=f"Poll created by: {context.message.author} • React to vote!"
        )
        embed_message = await context.send(embed=embed)
        await embed_message.add_reaction("⬆")
        await embed_message.add_reaction("⬇")


def setup(client):
    client.add_cog(Poll(client))
