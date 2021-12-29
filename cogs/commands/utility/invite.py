import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()


class Invite(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(name='invite', aliases=['addbot'], help="Invite the bot to your server")
	async def invite(self, ctx):
		em = discord.Embed(
			title="I'm glad you asked ```:D```",
			description=f"\nClick [here](https://top.gg/bot/899263193568936028) to add me to your server\nClick [here](https://discord.gg/BgmX5V8tQW) to join the support server."
		)
		em.set_thumbnail(url=self.client.user.avatar_url)
		em.set_footer(text='Bot created by <@663675391592103936>')

		await ctx.send(embed=em)


def setup(client):
	client.add_cog(Invite(client))