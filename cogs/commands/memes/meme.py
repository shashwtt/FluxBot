import random

import discord
import requests

import hex_colors

from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, Cog


class Meme(Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name='meme',
        aliases=['maymay', 'm'],
        help="Brings a post from meme subreddits..")
    @cooldown(1, 3, BucketType.user)
    async def meme(self, ctx):
        subreddits = ['memes', 'dankmemes']
        subreddit = random.choice(subreddits)
        url = f'https://meme-api.herokuapp.com/gimme/{subreddit}'
        response = requests.get(url)
        post = response.json()
        image = post['url']  # the meme (a reddit post)
        title = post['title']  # the title of the reddit post

        em = discord.Embed(
            title=title,
            color=random.choice(hex_colors.colors))
        em.set_image(url=image)
        em.set_footer(text=f"👍 {post['ups']} | Author: u/{post['author']}")

        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Meme(client))
