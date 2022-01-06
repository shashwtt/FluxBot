import json
import os

import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, Cog
import db


def get_prefix(guild):
	with open('prefix.json', 'r') as f:
		cache = json.load(f)

	guild = str(guild)

	if guild in cache:
		prefix = cache[guild]
	else:
		db.execute(f"SELECT prefix FROM Prefix WHERE guild = '{guild}'")
		prefix = db.fetchone()
		prefix = prefix[0]
		cache[str(guild)] = prefix

		with open('prefix.json', 'w') as g:
			json.dump(cache, g)

	return prefix


async def check_field(ctx, cog, _client):
	cog = cog.lower()
	if cog == "owner":
		if await _client.is_owner(ctx.author):
			return True
		else:
			return False
	return True


def get_working_cogs():
	cogs = []
	for cog in os.listdir("cogs/commands/"):
		if not os.path.isdir(cog):
			pass
		if not os.listdir(f"cogs/commands/{cog}"):
			pass
		cogs.append(cog.lower())
	return cogs


def decorate(command):
	args = []

	for key, value in command.params.items():
		if key not in ("self", "ctx"):
			if "None" in str(value) or "No reason provided" in str(value):
				args.append(f"[{key}]")
			else:
				args.append(f"<{key}>")

	args = " ".join(args)

	return f"```{command} {args}```"


class Help(Cog):
	def __init__(self, client):
		self.client = client
		self.aliases = {}
		for command in client.commands:
			self.aliases[f'{command}'] = str(command)
			for i in command.aliases:
				self.aliases[f'{i}'] = str(command)

	async def cmd_help(self, ctx, command):  # Makes the embed
		_aliases = ', '.join([*command.aliases])
		if _aliases == '':
			_aliases = "Command has no aliases"

		_help = command.help
		if _help is None:
			_help = 'No help text provided by developer'

		em = discord.Embed(title=str(command).capitalize(), description=command.help, color=0xf2cb7d)
		em.add_field(name='Usage:', value=decorate(command), inline=False)
		em.add_field(name='Aliases:', value=_aliases, inline=False)

		await ctx.send(embed=em)

	@commands.command(name="help")
	async def help(self, ctx, *, command_name=''):
		"""
		List all commands!
		"""
		prefix = get_prefix(ctx.guild.id)
		if command_name == "" or command_name is None:
			embed = discord.Embed(
				title="Help",
				description="Help on available commands..",
				color=0xf2cb7d,
			)
			embed.set_footer(text=f"Use {prefix}help <category> for more info")
			for cog in get_working_cogs():
				if await check_field(ctx, cog, self.client):
					commands = []
					help_text = ""
					for command in os.listdir(f"cogs/commands/{cog}"):
						if not command.endswith(".py"):
							continue
						command = command[:-3]
						commands.append(command)
					for command_list_str in commands:
						if command_list_str == "__pycache__":
							continue
						help_text = help_text + f"`{command_list_str}`, "
					embed.add_field(
						name=cog.capitalize(),
						value=help_text[:-2],
						inline=False
					)

			await ctx.send(f"{command_name}", embed=embed)
		elif command_name.startswith("<@") and command_name.endswith(">"):
			embed = discord.Embed(
				title="Bro, are you okay?",
				description="You are supposed to search for command here,\n mentioning someone doesn't make any sense!!"
			)
			await ctx.message.reply(embed=embed)
		else:

			if command_name in self.aliases:
				command_name = self.aliases[f"{command_name}"]
			else:
				embed = discord.Embed(
					title="Whoops!",
					description=f"I cannot find any command named `{command_name}`",
					color=0xff3344
				)
				await ctx.send(embed=embed)
				return

			command = discord.utils.get(self.client.commands, name=command_name)
			await self.cmd_help(ctx, command)


def setup(client):
	client.add_cog(Help(client))
