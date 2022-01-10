import discord
import hex_colors
import asyncio

from discord.ext import commands


class Nuke(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(name='nuke', help='Deletes the channel and makes a copy of it')
	@commands.has_permissions(manage_channels=True)
	@commands.bot_has_permissions(administrator=True)
	async def nuke(self, ctx, channel: discord.TextChannel = None):
		if channel is None:
			channel = ctx.channel

		reactions = {
			"✅": 0,
			"❌": 1
		}

		def check(reaction, user):
			return user == ctx.message.author and str(reaction) in reactions

		def cancel_click(Interaction):
			await choices.edit(embed=discord.Embed(title="Okay, cancelled the nuke!", colour=hex_colors.l_green), view=None)
			await choices.delete(delay=5)
			return

		def ok_click(Interaction):
			try:
				new_channel = await channel.clone(
					reason=f'Original was nuked by {ctx.author}')  # Reason to be registered in the audit log
				await new_channel.edit(position=channel.position)
				await channel.delete()

			except discord.Forbidden:
				await ctx.send(
					"I couldn't delete the channel, maybe this is a community updates channel?")  # Channels that are set for community updates cannot be deleted without transferring the community updates to another channel
				await new_channel.delete()  # The clone is useless if the original still exists

			em = discord.Embed(
				title='This channel got nuked!',
				description='Who did this? Check Audit Log',
				color=hex_colors.m_red)

			await new_channel.send(embed=em)

		view = discord.ui.View(timeout=15)
		ok_butt = discord.ui.Button(emoji="✅")
		ok_butt.callback = ok_click
		view.add_item(ok_butt)
		cancel_butt = discord.ui.Button(emoji="❌")
		cancel_butt.callback = cancel_click
		view.add_item(cancel_butt)

		confirmation = discord.Embed(
			title="Are you sure you want to proceed?",
			description=":white_check_mark: - Go ahead and Nuke\n\n:x: - Cancel the nuking!",
			color=0xF59E42
		)
		choices = await ctx.send(embed=confirmation, view=view)


def setup(client):
	client.add_cog(Nuke(client))
