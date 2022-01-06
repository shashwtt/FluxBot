import sys

import discord

from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, Cog


class Logs(Cog):
	def __init__(self, client):
		self.client = client

	@commands.is_owner()
	@commands.command(name="logs")
	async def ping(self, context):
		"""
		Get recent bot logs..
		"""
		log = open("../../../log.txt", "w+")
		log.write(str(sys.stdout))
		log.close()

		file = discord.File(
			fp="../../../log.txt",
			filename="Logs.txt",
			spoiler=True
		)
		await context.send(file=file)


def setup(client):
	client.add_cog(Logs(client))
