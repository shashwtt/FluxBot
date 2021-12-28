import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()


class Invite(commands.Cog):
	def __init__(self, client):
		self.perms = os.getenv("permissions")
		self.client = client

	@commands.command(name='invite', aliases=['addbot'], help="Invite the bot to your server")
	async def invite(self, ctx):
		em = discord.Embed(
			title="Thank you for inviting me",
			description=f"Click [here](https://discord.com/api/oauth2/authorize?client_id={self.client.user.id}&permissions={self.perms}&scope=bot) to add me to your server\nClick [here](https://discord.gg/TqSyUBhFFC) to join the support server."
		)
		em.set_thumbnail(url=self.client.user.avatar_url)
		em.set_footer(text='Bot created by <@663675391592103936>')

		await ctx.send(embed=em)


def setup(client):
	client.add_cog(Invite(client))