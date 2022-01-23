import discord
import random
import hex_colors

from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, Cog
from discord.ui import Button, View


class Avatar(Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(
		name='avatar',
		usage="[user]",
		aliases=['av', "pfp"],
		help="Show a user's avatar in full size",
		description="Maximize a user's avatar to download the image or just view it. If somebody wants to view other's avatar there is 10% chance a uno-reverse button will appear!"
	)
	@cooldown(1, 5, BucketType.user)
	async def avatar(self, ctx, user: discord.Member = None):

		member = user
		uno_reverse = True

		if member == ctx.author or member is None:
			uno_reverse = False

		if member is None:
			member = ctx.author

		reverse_butt = Button(emoji="<:uno_reverse:930372912584720434>")

		async def view_timeout():
			view.remove_item(reverse_butt)
			await mess.edit(embed=em, view=view)

		view = View(timeout=15)
		view.on_timeout = view_timeout
		em = discord.Embed(
			title=f"{member.display_name}'s avatar",
			color=random.choice(hex_colors.colors)
		)
		em.set_image(url=member.avatar.url)
		em.set_footer(text=f'Requested by {ctx.author.display_name}#{ctx.author.discriminator}')

		async def uno_reverse_callback(interaction):
			em2 = em
			em2.title = f"{ctx.author.display_name}'s avatar"
			em2.set_image(url=ctx.author.avatar.url)
			em2.set_footer(text=f"Reversed by {interaction.user.name}#{interaction.user.discriminator}")
			view2 = View()
			view2.add_item(Button(label="Download Image", url=f'{ctx.author.avatar.url}'))
			await interaction.response.edit_message(embed=em2, view=view2)

		if uno_reverse:
			chance = random.randrange(1, 10)
			if chance == 10:
				reverse_butt.callback = uno_reverse_callback
				view.add_item(reverse_butt)

		download_button = Button(label="Download Image", url=f"{member.avatar.url}")
		view.add_item(download_button)

		mess = await ctx.send(embed=em, view=view)


def setup(client):
	client.add_cog(Avatar(client))
