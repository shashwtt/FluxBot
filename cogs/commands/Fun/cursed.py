import random

import discord
import requests

import hex_colors

from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, Cog


class Cursed(Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='cursed', aliases=['cursedimage'], help="Brings a post from r/cursed_images")
    @cooldown(1, 3, BucketType.user)
    async def cursed_image(self, ctx):
        url = f'https://meme-api.herokuapp.com/gimme/cursed_images'  # url of the api
        """
        There is reddit's official API too, but it's slower and also sometimes returns mp4(s) that the discord.Embed class can't process. This API is much better in my opinion. Also, both, this and reddit's API are free.
        """

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
    client.add_cog(Cursed(client))
