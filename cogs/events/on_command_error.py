import json
import random

import discord
from db import *
from discord.ext import commands


def get_prefix(guild):
	with open('prefix.json', 'r') as f:
		cache = json.load(f)

	guild = str(guild)

	if guild in cache:
		prefix = cache[guild]
	else:
		cur.execute(f"SELECT prefix FROM Prefix WHERE guild = '{guild}'")
		prefix = cur.fetchone()
		prefix = prefix[0]
		cache[str(guild)] = prefix

		with open('prefix.json', 'w') as g:
			json.dump(cache, g)

	return prefix


def usage(command):
	args = []

	for key, value in command.params.items():
		if key not in ("self", "ctx"):
			if "None" in str(value) or "No reason provided" in str(value):
				args.append(f"[{key}]")
			else:
				args.append(f"<{key}>")

	args = " ".join(args)

	return f"```{command} {args}```"


class ErrorHandling(commands.Cog):
	def __init__(self, client):
		self.client = client
		with open("config.json", 'r') as config_file:
			self.config = json.load(config_file)
			config_file.close()

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):

		if isinstance(error, commands.MissingRequiredArgument):
			em = discord.Embed(
				title='Command incomplete!',
				color=discord.Color.brand_red(),
				description=f"This command is missing some arguements.. \n\n **Usage -** {usage(ctx.command)}"
			)

			await ctx.reply(embed=em, mention_author=False)
			ctx.command.reset_cooldown(ctx)
			return

		elif isinstance(error, commands.MissingPermissions):

			# This part is copy-pasted from a different source (I don't remember where.)
			missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_permissions]

			if len(missing) > 2:
				permission = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
			else:
				permission = ' and '.join(missing)

			em = discord.Embed(
				title='Missing Permissions!',
				description=f"You need the `{permission}` permission to do that",
				color=discord.Color.brand_red()
			)
			await ctx.reply(embed=em, mention_author=False)
			return

		elif isinstance(error, commands.MemberNotFound):
			not_found = [
				"**What are you talking about??** \n\nNo such person exists on this server...",
				"I searched through the deepest places of this server and still\n `I cannot find the person you mentioned`",
				"Welp, this person is no longer in existence, Go find somebody else!"
			]
			em = discord.Embed(
				description=random.choice(not_found),
				color=discord.Color.brand_red())

			await ctx.reply(embed=em, mention_author=False)
			ctx.command.reset_cooldown(ctx)
			return

		elif isinstance(error, commands.BotMissingPermissions):
			mp = error.missing_permissions[0]
			mp = mp.title()
			mp = mp.replace('_', ' ')

			em = discord.Embed(
				description=f"This should have worked but I have some permissions missing...\n\nMissing Permission - `{mp}`",
				color=discord.Color.brand_red())

			try:
				await ctx.send(embed=em)
				return
			except discord.Forbidden:
				await ctx.send(
					f"I don't have the {mp} permission. F")  # In case the bot doesn't have embed links permission
			return

		elif isinstance(error, commands.CommandOnCooldown):
			mode = "second(s)"
			if error.retry_after > 120:
				error.retry_after = error.retry_after // 60
				mode = "minute(s)"

			if error.retry_after > 3600:
				error.retry_after = error.retry_after // 3600
				mode = "hour(s)"

			em = discord.Embed(
				title="Whoa there, hold your horses!",
				description=f"The `{ctx.command}` command is on a cooldown, try again in **{error.retry_after:,.1f} {mode}**",
				colour=discord.Color.brand_red())
			await ctx.reply(embed=em, mention_author=False)
			return

		elif isinstance(error, commands.BadArgument):
			em = discord.Embed(title="Invalid arguments!", color=discord.Color.brand_red(),
			                   description=f"I think you used the command wrong. For more info, try running: ```{get_prefix(ctx.guild.id)}help {ctx.command}```")
			await ctx.send(embed=em)
			ctx.command.reset_cooldown(ctx)
			return

		elif isinstance(error, commands.CommandNotFound):
			return

		elif isinstance(error, discord.Forbidden):
			try:
				em = discord.Embed(
					title='Missing Permissions',
					description="**Error code 403 Forbidden was raised. I can't do anything here...** \n\nContact my developers or join support server for help",
					color=discord.Color.brand_red()
				)
				ctx.reply(embed=em, mention_author=False)
				return
			except discord.Forbidden:
				await ctx.reply("I need the 'Embed Links' permission.")
				return

		else:
			await ctx.reply(embed=discord.Embed(
				title="Something went Wrong!!",
				description="An error occurred that I wasn't able to handle myself. This has been conveyed to my developer.",
				color=discord.Color.brand_red()
			))
			channel = self.client.get_channel(self.config['err_channel'])

			em = discord.Embed(title='Error', color=0xFF3E3E)

			em.add_field(name='Command', value=ctx.command, inline=False)
			em.add_field(name='Error:', value=f"```{type(error)}\n{error}```", inline=False)
			em.add_field(name='Server:', value=f"{ctx.guild} ({ctx.guild.id})", inline=False)
			em.add_field(name='Channel:', value=f"{ctx.channel} ({ctx.channel.id})", inline=False)
			em.add_field(name='User:', value=f"{ctx.author} ({ctx.author.id})", inline=False)
			em.add_field(name='Message:', value=ctx.message.content)

			view = discord.ui.View()
			try:
				link = await ctx.channel.create_invite(
					temporary=True,
					reason="Invite link to be sent to the bot developer.. for error report!"
				)
				invite_butt = discord.ui.Button(label="Visit server", url=link.url)
				view.add_item(invite_butt)
			except discord.HTTPException or discord.NotFound:
				invite_butt = discord.ui.Button(label="Can't create invite", disabled=True)
				view.add_item(invite_butt)

			await channel.send(embed=em, view=view)


def setup(client):
	client.add_cog(ErrorHandling(client))
