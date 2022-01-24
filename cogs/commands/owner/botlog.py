import discord
import heroku3
import urllib3
from io import BytesIO

from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, Cog

urllib3.disable_warnings()


class BotLog(Cog):
	def __init__(self, client):
		self.client = client
		self.heroku_ = heroku3.from_key('15f0ed8e-5a8d-4c50-81df-7f6200e26df6')

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
				description=f"Last {lines} lines of log by the bot from heroku app `flux-discord`\n\n Bot Logs - ```prolog \n {logs}```",
				color=discord.Color.orange()
			))
		else:
			await ctx.author.send(embed=discord.Embed(
				description=f"Last {lines} lines of log by the bot from heroku app `flux-discord`",
				color=discord.Color.orange()
			), file=discord.File(BytesIO(content), "logs.log"))

		await ctx.send(embed=discord.Embed(
			description="<:flux_check:934693030592655411> I have sent you a private message!",
			color=discord.Color.brand_green()
		))


def setup(client):
	client.add_cog(BotLog(client))
