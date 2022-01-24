import discord
import heroku3
import urllib3
from io import BytesIO
from dotenv import load_dotenv

from discord.ext import commands
import os
from discord.ext.commands import cooldown, BucketType, Cog


load_dotenv()
heroku_key = os.getenv("heroku_key")
urllib3.disable_warnings()


class BotLog(Cog):
	def __init__(self, client):
		self.client = client
		self.heroku_ = heroku3.from_key(heroku_key)

	@commands.is_owner()
	@commands.command(
		name="botlog",
		aliases=["heroku-log"],
		usage="[lines]",
		help="Get bot logs - errors, warning, messages, etc.",
		description="Get the logs of the discord bot. If the number of lines is not defined then it defaults to 25 lines of most recent logs"
	)
	async def botlog(self, ctx, lines: int = 0):
		if lines == 0:
			lines = 25

		logs = self.heroku_.get_app_log("flux-discord", lines=lines)
		as_bytes = map(str.encode, logs)
		content = b"".join(as_bytes)

		if len(logs) < 1900:
			await ctx.author.send(embed=discord.Embed(
				description=f"Last {lines} lines of log by the bot from heroku app `flux-discord`",
				color=discord.Color.purple()
			), content=f'''```accesslog
{logs}```''')
		else:
			await ctx.author.send(embed=discord.Embed(
				description=f"Last {lines} lines of log by the bot from heroku app `flux-discord`",
				color=discord.Color.purple()
			), file=discord.File(BytesIO(content), "logs.log"))

		await ctx.send(embed=discord.Embed(
			description="<:flux_check:934693030592655411> I have sent you a private message!",
			color=discord.Color.brand_green()
		))


def setup(client):
	client.add_cog(BotLog(client))
