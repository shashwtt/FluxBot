import sys

import discord

from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, Cog


class Logs(Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(name="logs")
	async def ping(self, context):
		"""
		Get recent bot logs..
		"""
		await context.send(f"")


def setup(client):
	client.add_cog(Logs(client))
