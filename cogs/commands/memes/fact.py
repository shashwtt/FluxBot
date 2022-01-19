import aiohttp
import discord
import hex_colors

from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, Cog


def bool_str(variable):  # Function to convert boolean values to string: Yes/No
    if variable:
        return 'Yes'
    if not variable:
        return 'No'


class Fact(Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name="fact",
        brief="fact",
        aliases=["faxx"])
    async def fact(self, context):
        """
        Get a useless fact, They're pretty good!
        """
        # This will prevent your bot from stopping everything when doing a web request - see:
        # https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with aiohttp.ClientSession() as session:
            async with session.get("https://uselessfacts.jsph.pl/random.json?language=en") as request:
                if request.status == 200:
                    data = await request.json()
                    fact = data['text']
                    embed = discord.Embed(description=fact, color=0xD75BF4)
                    await context.send(embed=embed)
                else:
                    self.dailyfact.reset_cooldown(context)


def setup(client):
    client.add_cog(Fact(client))
