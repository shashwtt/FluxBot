import aiohttp
import discord
import hex_colors

from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, Cog


class Ping(Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(name="ping", aliases=["latency"])
	async def ping(self, context):
		"""
		Check if the bot is alive.
		"""
		embed = discord.Embed(
			title="🏓 Pong!",
			description=f"The bot latency is {round(self.client.latency * 1000)}ms.",
			color=0x42F56C
		)
		await context.send(embed=embed)
		print(open("../../../output.log", "r").read())


def setup(client):
	client.add_cog(Ping(client))
