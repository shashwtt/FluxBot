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

    async def edit_meme_new(self, ctx, interaction):
        async def next_meme_callback(msg_inter):
            await self.edit_meme_new(ctx, msg_inter)

        async def close_meme_view(msg_inter=None):
            meme_view.stop()
            meme_view.clear_items()
            if msg_inter is None:
                await interaction.message.edit(view=None)
            else:
                await msg_inter.message.edit(view=None)

        meme = get_meme()
        post = meme[0]
        image = meme[1]
        title = meme[2]

        meme_view = discord.ui.View(timeout=15)
        next_meme = discord.ui.Button(label="Next meme!", style=discord.ButtonStyle.green)
        next_meme.callback = next_meme_callback
        close_view = discord.ui.Button(emoji="<:x_white:930381127535984641>", style=discord.ButtonStyle.danger)
        close_view.callback = close_meme_view
        meme_view.add_item(next_meme)
        meme_view.add_item(close_view)
        meme_view.on_timeout = close_meme_view

        ctx.message.embeds[0].title = title
        ctx.message.embeds[0].set_imgage(url=image)
        ctx.message.embeds[0].set_footer(text=f"👍 {post['ups']} | Posted by - [u/{post['author']}](https://www.reddit.com/u/{post['author']})")

        await interaction.message.edit(embed=ctx.message.embeds[0], view=meme_view)

    @commands.command(name='meme', aliases=['maymay', 'm'], help="Brings a post from meme subreddits..")
    @cooldown(1, 3, BucketType.user)
    async def meme(self, ctx):
        async def next_meme_callback(interaction):
            await self.edit_meme_new(ctx, interaction)

        async def close_meme_view(interaction=None):
            meme_view.stop()
            meme_view.clear_items()
            if interaction is None:
                message.edit(view=None)
            else:
                await interaction.message.edit(view=None)

        meme = get_meme()
        post = meme[0]
        image = meme[1]
        title = meme[2]
        meme_view = discord.ui.View(timeout=15)
        next_meme = discord.ui.Button(label="Next meme!", style=discord.ButtonStyle.green)
        next_meme.callback = next_meme_callback
        close_view = discord.ui.Button(emoji="<:x_white:930381127535984641>", style=discord.ButtonStyle.danger)
        close_view.callback = close_meme_view
        meme_view.add_item(next_meme)
        meme_view.add_item(close_view)
        meme_view.on_timeout = close_meme_view

        em = discord.Embed(
            title=title,
            color=random.choice(hex_colors.colors))
        em.set_image(url=image)
        em.set_footer(text=f"👍 {post['ups']} | Author: u/{post['author']}")

        message = await ctx.send(embed=em, view=meme_view)


def setup(client):
    client.add_cog(Meme(client))
