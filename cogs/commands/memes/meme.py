import random

import discord
import requests

import hex_colors

from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, Cog


def get_meme():
    subreddits = ['memes', 'dankmemes']
    subreddit = random.choice(subreddits)
    url = f'https://meme-api.herokuapp.com/gimme/{subreddit}'
    response = requests.get(url)
    post = response.json()
    image = post['url']  # the meme (a reddit post)
    title = post['title']  # the title of the reddit post

    return [post, image, title]


class Meme(Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name='meme',
        aliases=['maymay', 'm'],
        help="Brings a post from meme subreddits..")
    @cooldown(1, 3, BucketType.user)
    async def meme(self, ctx):

        async def next_meme_callback(interaction):
            x = await send_meme()
            interaction.message.edit(embed=x[0], view=x[1])

        async def send_meme():
            meme = get_meme()
            post = meme[0]
            image = meme[1]
            title = meme[2]
            meme_view = discord.ui.View(timeout=15)
            next_meme = discord.ui.Button(label="Next meme!", style=discord.ButtonStyle.green)
            next_meme.callback = next_meme_callback
            meme_view.add_item(next_meme)

            em = discord.Embed(
                title=title,
                color=random.choice(hex_colors.colors))
            em.set_image(url=image)
            em.set_footer(text=f"👍 {post['ups']} | Author: u/{post['author']}")
            return [em, meme_view]

        x = await send_meme()
        ctx.send(embed=x[0], view=x[1])


def setup(client):
    client.add_cog(Meme(client))
