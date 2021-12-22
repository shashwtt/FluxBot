import asyncio
import json
import os
import random
import sys

import hex_colors
import requests
import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

if not os.path.isfile("config.json"):
	sys.exit("'config.json' not found! Please add it and try again.")
else:
	with open("config.json") as file:
		config = json.load(file)


class Fun(commands.Cog, name="fun"):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(
		name="fact",
		brief="fact",
		aliases=["faxx"])
	async def dailyfact(self, context):
		"""
		Get a daily fact, once per day!
		"""
		# This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
		async with aiohttp.ClientSession() as session:
			async with session.get("https://uselessfacts.jsph.pl/random.json?language=en") as request:
				if request.status == 200:
					data = await request.json()
					embed = discord.Embed(description=data["text"], color=0xD75BF4)
					await context.send(embed=embed)
				else:	
					self.dailyfact.reset_cooldown(context)

	@commands.command(
		name='reddit', 
		aliases=['subreddit', 'getredditpost'], 
		help='Gets a post from the subreddit provided',
		brief="reddit <sub-reddit>")
	@commands.cooldown(1, 3, commands.BucketType.user)
	async def get_reddit_post(self, ctx, *, subreddit):
		url = f'https://meme-api.herokuapp.com/gimme/{subreddit}'  # This api only sends posts with images or gifs.

		post = requests.get(url=url).json()
		# Check if the post is nsfw
		if 'nsfw' in post:  # Sometimes it raises KeyError
			if post['nsfw']:
				if not ctx.channel.is_nsfw():
					await ctx.send("The post I got from that subreddit is marked NSFW. I cannot send it here")
					return

		try:
			image = post['url']  # the image
			title = post['title']  # the title of the reddit post
			link = post['postLink']  # the link to the post

			em = discord.Embed(
				title=f"[{title}]({link})",
				color=random.choice(hex_colors.colors)
			)
			em.set_image(url=image)
			em.set_footer(
				text=f"👍 {post['ups']} | Author: u/{post['author']}")  # post['ups'] is the upvote count, post['author'] is the author

			await ctx.send(embed=em)

		except KeyError as e:
			if post["code"] == 400:
				if "no posts with images" in post["message"].lower():
					await ctx.send("That subreddit doesn't have any posts with images")
					return

			if post["code"] == 404:
				await ctx.send("This subreddit has no posts or doesn't exist.")
				return

	@commands.command(
		name='roast', 
		aliases=['insult'], 
		help="Roast someone. hehe",
		brief="roast [user]")
	async def roast(self, ctx, user:discord.Member=None):
		if user is None:
			user = ctx.author 

		if user.bot:
			await ctx.send("I'm not gonna roast someone of my own kind!")
			return

		url = 'https://insult.mattbas.org/api/en/insult.json' #Visit [https://insult.matlabs.org/api/] for documentation
		response = requests.get(url, params={'who': user.mention}).json()
		await ctx.send(user.mention+response['insult'])

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

	@commands.command(name="rps", help="Play rock, paper, scissors with me :)", aliases = ["rockpaperscissors"])
	async def rock_paper_scissors(self, context):
		choices = {
			0: "rock",
			1: "paper",
			2: "scissors"
		}
		reactions = {
			"🪨": 0,
			"🧻": 1,
			"✂": 2
		}
		embed = discord.Embed(title="Please choose", color=0xF59E42)
		embed.set_author(name=context.author.display_name, icon_url=context.author.avatar_url)
		choose_message = await context.send(embed=embed)
		for emoji in reactions:
			await choose_message.add_reaction(emoji)

		def check(reaction, user):
			return user == context.message.author and str(reaction) in reactions

		try:
			reaction, user = await self.bot.wait_for("reaction_add", timeout=10, check=check)

			user_choice_emote = reaction.emoji
			user_choice_index = reactions[user_choice_emote]

			bot_choice_emote = random.choice(list(reactions.keys()))
			bot_choice_index = reactions[bot_choice_emote]

			result_embed = discord.Embed(color=0x42F56C)
			result_embed.set_author(name=context.author.display_name, icon_url=context.author.avatar_url)
			await choose_message.clear_reactions()

			if user_choice_index == bot_choice_index:
				result_embed.description = f"**That's a draw!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
				result_embed.colour = 0xF59E42
			elif user_choice_index == 0 and bot_choice_index == 2:
				result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
				result_embed.colour = 0x42F56C
			elif user_choice_index == 1 and bot_choice_index == 0:
				result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
				result_embed.colour = 0x42F56C
			elif user_choice_index == 2 and bot_choice_index == 1:
				result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
				result_embed.colour = 0x42F56C
			else:
				result_embed.description = f"**I won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
				result_embed.colour = 0xE02B2B
				await choose_message.add_reaction("🇱")
			await choose_message.edit(embed=result_embed)
		except asyncio.exceptions.TimeoutError:
			await choose_message.clear_reactions()
			timeout_embed = discord.Embed(title="Too late", color=0xE02B2B)
			timeout_embed.set_author(name=context.author.display_name, icon_url=context.author.avatar_url)
			await choose_message.edit(embed=timeout_embed)

	@commands.command(name='cursed', aliases=['cursedimage'], help="Brings a post from r/cursed_images")
	@cooldown(1, 3, BucketType.user)
	async def cursed_image(self, ctx):
		url = f'https://meme-api.herokuapp.com/gimme/cursed_images' #url of the api
		"""
		There is reddit's official API too, but it's slower and also sometimes returns mp4(s) that the discord.Embed class can't process. This API is much better in my opinion. Also, both, this and reddit's API are free.
		"""

		response = requests.get(url)
		post = response.json()
		image = post['url'] #the meme (a reddit post)
		title = post['title'] #the title of the reddit post


		em = discord.Embed(
			title=title,
			color=random.choice(hex_colors.colors))
		em.set_image(url=image)
		em.set_footer(text=f"👍 {post['ups']} | Author: u/{post['author']}")

		await ctx.send(embed=em)
	
	@commands.command(name="poll", aliases=["vote"])
	async def poll(self, context, *, title):
		"""
		Create a poll where members can vote.
		"""
		embed = discord.Embed(
			title="A new poll has been created!",
			description=f"{title}",
			color=0x42F56C
		)
		embed.set_footer(
			text=f"Poll created by: {context.message.author} • React to vote!"
		)
		embed_message = await context.send(embed=embed)
		await embed_message.add_reaction("👍")
		await embed_message.add_reaction("👎")
		await embed_message.add_reaction("🤷")

	@commands.command(name="8ball", aliases=["8b"])
	async def eight_ball(self, context, *, question):
		"""
		Ask any question to the bot.
		"""
		answers = ['It is certain.', 'It is decidedly so.', 'You may rely on it.', 'Without a doubt.',
				   'Yes - definitely.', 'As I see, yes.', 'Most likely.', 'Outlook good.', 'Yes.',
				   'Signs point to yes.', 'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.',
				   'Cannot predict now.', 'Concentrate and ask again later.', 'Don\'t count on it.', 'My reply is no.',
				   'My sources say no.', 'Outlook not so good.', 'Very doubtful.', "nah"]
		embed = discord.Embed(
			title="**My Answer:**",
			description=f"{answers[random.randint(0, len(answers))]}",
			color=0x42F56C
		)
		embed.set_footer(
			text=f"The question was: {question}"
		)
		await context.send(embed=embed)

def setup(bot):
	bot.add_cog(Fun(bot))
