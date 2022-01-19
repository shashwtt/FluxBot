import asyncio
import random
import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, Cog
from discord.ui import View, Button

import hex_colors

reactions = ["🪨", "🧻", "✂"]


async def work(ctx, user_choice_index, interaction: discord.Interaction, view,client_, enemy_index: int = None, enemy=None):
	enemy_choice_index = enemy_index
	if enemy_index is None:
		enemy_choice_index = random.randint(0, 2)
	enemy_choice_emote = reactions[enemy_choice_index]
	user_choice_emote = reactions[user_choice_index]

	result_embed = discord.Embed()

	if user_choice_index == enemy_choice_index:
		result_embed.description = f"**That's a draw!**\n You both had the same choice - {user_choice_emote}"
		if enemy is None:
			result_embed.description = f"**That's a draw** Our choice was the same - {user_choice_emote}"
		result_embed.colour = hex_colors.l_yellow
	elif user_choice_index == 0 and enemy_choice_index == 2:
		result_embed.description = f"**You won!**\nYou chose {user_choice_emote} and {enemy}'s choice was {enemy_choice_emote}."
		if enemy is None:
			result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {enemy_choice_emote}."
		result_embed.colour = hex_colors.l_green
	elif user_choice_index == 1 and enemy_choice_index == 0:
		result_embed.description = f"**You won!**\nYou chose {user_choice_emote} and {enemy}'s choice was {enemy_choice_emote}."
		if enemy is None:
			result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {enemy_choice_emote}."
		result_embed.colour = hex_colors.l_green
	elif user_choice_index == 2 and enemy_choice_index == 1:
		result_embed.description = f"**You won!**\nYou chose {user_choice_emote} and {enemy}'s choice was {enemy_choice_emote}."
		if enemy is None:
			result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {enemy_choice_emote}."
		result_embed.colour = hex_colors.l_green
	else:
		result_embed.description = f"**{enemy} won!**\nYou chose {user_choice_emote} while {enemy}'s choice was {enemy_choice_emote}."
		if enemy is None:
			result_embed.description = f"**I won!**\nYou've chosen {user_choice_emote} and I've chosen {enemy_choice_emote}."
		result_embed.colour = 0xE02B2B

	view.stop()
	view9 = View(timeout=10)
	async def timeup():
		view9.clear_items()
		interaction.response.edit_message(embed=result_embed, view=None)
		view9.stop()

	async def reboot(interactionn):
		view9.clear_items()
		interactionn.response.edit_message(embed=result_embed, view=None)
		view9.stop()
		await RPS(client_).rock_paper_scissors(ctx, boi=enemy)

	view9.on_timeout = timeup
	btn = Button(
		label=f"{random.choice(['Once more!', 'Play again!', 'Moree!'])}",
		style=discord.ButtonStyle.green
	)
	btn.callback = reboot
	view9.add_item(btn)
	await interaction.response.edit_message(embed=result_embed, view=view9)


class MySoloView(View):
	def __init__(self, ctx, timeout, client_):
		super(MySoloView, self).__init__(timeout=timeout)
		self.ctx = ctx
		self.client_ = client_

	@discord.ui.button(style=discord.ButtonStyle.blurple, emoji=f"{reactions[0]}")
	async def button_click0(self, button, interaction):
		button.disabled = True
		await work(self.ctx, 0, interaction, self, self.client_)

	@discord.ui.button(style=discord.ButtonStyle.blurple, emoji=f"{reactions[1]}")
	async def button_click1(self, button, interaction):
		button.disabled = True
		await work(self.ctx, 1, interaction, self, self.client_)

	@discord.ui.button(style=discord.ButtonStyle.blurple, emoji=f"{reactions[2]}")
	async def button_click2(self, button, interaction):
		button.disabled = True
		await work(self.ctx, 2, interaction, self, self.client_)

	async def view_timeout(self) -> None:
		pass


class RPS(Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(
		name="rps",
		help="Play a calm game of rock, paper, scissors with me :)",
		aliases=["rockpaperscissors"]
	)
	@cooldown(1, 2, BucketType.user)
	async def rock_paper_scissors(self, ctx, boi: discord.Member = None):
		view = MySoloView(ctx, timeout=10, client_=self.client)

		if boi is None or boi is self.client.user:
			embed = discord.Embed(
				title=f"{ctx.author.display_name} vs {self.client.user.display_name}",
				color=0xF59E42
			)
			embed.add_field(name=f"{ctx.author.display_name}", value=" -> Choosing his move...\n", inline=False)
			embed.add_field(name=f"{self.client.user.display_name}", value="-> `Ready!!`", inline=False)
			embed.set_footer(text='You have 10 seconds to choose!')

			choose_message = await ctx.send(embed=embed, view=view)

			async def view_timeup(msg):
				timeout_embed = discord.Embed(title="Too late", color=0xE02B2B)
				timeout_embed.set_author(name=self.ctx.author.display_name, icon_url=self.ctx.author.avatar.url)
				await choose_message.edit(embed=timeout_embed, view=None)

			view.on_timeout = view_timeup


def setup(client):
	client.add_cog(RPS(client))
