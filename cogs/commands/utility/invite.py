import discord
from dotenv import load_dotenv
from discord.ui import Button, View
from discord.ext import commands

load_dotenv()


class Invite(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(name='invite', aliases=['addbot'], help="Invite the bot to your server")
	async def invite(self, ctx):
		owner = await self.client.fetch_user(int(self.client.owner_ids[0]))
		em = discord.Embed(
			title="I'm glad you asked ```:D```",
			description=f"\nClick [here](https://top.gg/bot/899263193568936028) to add me to your server\nClick ["
			f"here](https://discord.gg/BgmX5V8tQW) to join the support server. \n\n Bot created by - <@{owner.id}>"
		)
		em.set_thumbnail(url=self.client.user.avatar.url)
		add_bot_button = Button(label="Invite Bot", url="https://discord.com/api/oauth2/authorize?client_id=899263193568936028&permissions=0&scope=bot")
		joinserver_button = Button(label="Join Support Server", url="https://discord.gg/BgmX5V8tQW")

		view = View()
		view.add_item(add_bot_button)
		view.add_item(joinserver_button)
		await ctx.send(embed=em, view=view)


def setup(client):
	client.add_cog(Invite(client))
