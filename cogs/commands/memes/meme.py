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

	@commands.command(name='meme', aliases=['maymay', 'm'], help="Brings a post from meme subreddits..")
	@cooldown(1, 3, BucketType.user)
	async def meme(self, ctx):
		async def next_meme_callback(interaction):
			my_meme = get_meme()
			may = my_meme[0]
			memage = my_meme[1]
			mimle = my_meme[2]
			membed = interaction.message.embeds[0]
			membed.set_image(url=memage)
			membed.title = mimle
			membed.set_footer(text=f"👍 {may['ups']} | Author: u/{may['author']}")
			membed.color = random.choice(hex_colors.colors)

			await interaction.message.edit(embed=membed)

		async def close_meme_view(interaction):
			await interaction.message.edit(view=None)

		async def timeout_view():
			await message.edit(view=None)

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
		meme_view.on_timeout = timeout_view

		em = discord.Embed(
			title=title,
			color=random.choice(hex_colors.colors))
		em.set_image(url=image)
		em.set_footer(text=f"👍 {post['ups']} | Author: u/{post['author']}")

		message = await ctx.send(embed=em, view=meme_view)


def setup(client):
	client.add_cog(Meme(client))
