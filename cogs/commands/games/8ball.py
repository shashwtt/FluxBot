import random

import discord
import requests

import hex_colors

from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, Cog


class YesNo(Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="8ball", aliases=["8b", "yesno"])
    async def eight_ball(self, context, *, question):
        """
        Ask any question to the bot.
        """
        answers = ['It is certain.', 'It is decidedly so.', 'You may rely on it.', 'Without a doubt.',
                   'Yes - definitely.', 'As I see, yes.', 'Most likely.', 'Outlook good.', 'Yes.',
                   'Signs point to yes.', 'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.',
                   'Cannot predict now.', 'Concentrate and ask again later.', 'Don\'t count on it.', 'My reply is no.',
                   'My sources say no.', 'Outlook not so good.', 'Very doubtful.', "nah", '...', 'lol']
        embed = discord.Embed(
            title=f"{question}",
            description=f"```{answers[random.randint(0, len(answers))]}```",
            color=0x42F56C
        )
        await context.send(embed=embed)


def setup(client):
    client.add_cog(YesNo(client))
