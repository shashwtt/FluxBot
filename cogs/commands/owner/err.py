import discord

from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, Cog


class Err(Cog):
	def __init__(self, client):
		self.client = client

	@commands.is_owner()
	@commands.command(name="err", help="Raise errors, wait whaa..")
	async def err(self, ctx, *, err_name):
		errors = {
			'ApplicationCommandError': discord.ApplicationCommandError,
			'ExtensionError': discord.ExtensionError,
			'HttpException': discord.HTTPException,
			'NotFound': discord.NotFound,
			'Forbidden': discord.Forbidden,
			'ApplicationCommandInvokeError': discord.ApplicationCommandInvokeError,
		}
		_shards = self.client.shards
		await ctx.send(str(_shards))




def setup(client):
	client.add_cog(Err(client))
