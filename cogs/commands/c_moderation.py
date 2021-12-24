import json
import os
import sys
import traceback

import discord
from discord import member
from discord.ext import commands

if not os.path.isfile("config.json"):
	sys.exit("'config.json' not found! Please add it and try again.")
else:
	with open("config.json") as file:
		config = json.load(file)


class moderation(commands.Cog, name="moderation"):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='kick', pass_context=True)
	@commands.has_permissions(kick_members=True)
	async def kick(self, context, member: discord.Member, *, reason="Not specified"):
		"""
		Kick a user out of the server.
		"""
		if member.guild_permissions.administrator:
			embed = discord.Embed(
				title="Error!",
				description="User has Admin permissions.",
				color=0xE02B2B
			)
			await context.send(embed=embed)
		else:
			try:
				await member.kick(reason=reason)
				embed = discord.Embed(
					title="User Kicked!",
					description=f"**{member}** was kicked by **{context.message.author}**!",
					color=0x42F56C
				)
				embed.add_field(
					name="Reason:",
					value=reason
				)
				await context.send(embed=embed)
				try:
					await member.send(
						f"You were kicked by **{context.message.author}**!\nReason: {reason}"
					)
				except:
					pass
			except:
				embed = discord.Embed(
					title="Error!",
					description="An error occurred while trying to kick the user. Make sure my role is above the role of the user you want to kick.",
					color=0xE02B2B
				)
				await context.message.channel.send(embed=embed)


	@commands.command(name="nick")
	@commands.has_permissions(manage_nicknames=True)
	async def nick(self, context, member: discord.Member, *, nickname=None):
		"""
		Change the nickname of a user on a server.
		"""
		try:
			await member.edit(nick=nickname)
			embed = discord.Embed(
				title="Changed Nickname!",
				description=f"**{member}'s** new nickname is **{nickname}**!",
				color=0x42F56C
			)
			await context.send(embed=embed)
		except:
			embed = discord.Embed(
				title="Error!",
				description="An error occurred while trying to change the nickname of the user. Make sure my role is above the role of the user you want to change the nickname.",
				color=0xE02B2B
			)
			await context.message.channel.send(embed=embed)

	@commands.command(name="ban")
	@commands.has_permissions(ban_members=True)
	async def ban(self, context, member: discord.Member, *, reason="Not specified"):
		"""
		Bans a user from the server.
		"""
		try:
			if member.guild_permissions.administrator:
				embed = discord.Embed(
					title="Error!",
					description="User has Admin permissions.",
					color=0xE02B2B
				)
				await context.send(embed=embed)
			else:
				await member.ban(reason=reason)
				embed = discord.Embed(
					title="User Banned!",
					description=f"**{member}** was banned by **{context.message.author}**!",
					color=0x42F56C
				)
				embed.add_field(
					name="Reason:",
					value=reason
				)
				await context.send(embed=embed)
				await member.send(f"You were banned by **{context.message.author}**!\nReason: {reason}")
		except:
			embed = discord.Embed(
				title="Error!",
				description="An error occurred while trying to ban the user. Make sure my role is above the role of the user you want to ban.",
				color=0xE02B2B
			)
			await context.send(embed=embed)

	@commands.command(name='nuke', help='Deletes the channel and makes a copy of it')
	@commands.has_permissions(manage_channels=True)
	@commands.bot_has_permissions(administrator=True)
	async def nuke(self, ctx):
		existing_channel = ctx.channel

		new_channel = await existing_channel.clone(reason=f'Original was nuked by {ctx.author}') #Reason to be registered in the audit log
		await new_channel.edit(position=existing_channel.position)
		try:
			await ctx.channel.delete()
		except discord.Forbidden:
			await ctx.send("I couldn't delete the channel, maybe this is a community updates channel?") #Channels that are set for community updates cannot be deleted without transferring the community updates to another channel

		em = discord.Embed(
                    title='This channel got nuked!',
                    description='Who did this? Check Audit Log',
                    color=0xFF3E3E)

		await new_channel.send(embed=em)

	@commands.command(name="warn")
	@commands.has_permissions(manage_messages=True)
	async def warn(self, context, member: discord.Member, *, reason="Not specified"):
		"""
		Warns a user in his private messages.
		"""
		embed = discord.Embed(
			title="User Warned!",
			description=f"**{member}** was warned by **{context.message.author}**!",
			color=0x42F56C
		)
		embed.add_field(
			name="Reason:",
			value=reason
		)
		await context.send(embed=embed)
		try:
			await member.send(f"You were warned by **{context.message.author}**!\nReason: {reason}")
		except:
			pass

	@commands.command(name='clear', aliases=['delete','purge','prune', "del"], help='Mass delete messages')
	@commands.bot_has_permissions(manage_messages=True)
	@commands.has_permissions(manage_messages=True)
	async def clear(self, ctx, amount=1):
		if amount <= 0: #The number needs to be more than 0
			await ctx.send("I'm kinda confused")
			return

		if amount > 200:
			await ctx.send("Now, I could do that, but discord doesn't like it when I do that.")
			return

		await ctx.channel.purge(limit=amount+1) #Amount +1 because the command message is also included
		await ctx.send(f"**{ctx.author.name}** deleted {amount} messages", delete_after=3)


def setup(bot):
	bot.add_cog(moderation(bot))