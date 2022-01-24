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
        self.flux_app = self.heroku_.app("flux-discord")

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

        logs = self.flux_app.get_logs(lines=lines)
        as_bytes = map(str.encode, logs)
        content = b"\n".join(as_bytes)
        await ctx.send(f"`Most recent {lines} of logs from app flux-discord - `", file=discord.File(BytesIO(content), "logs.txt"))


def setup(client):
    client.add_cog(BotLog(client))
