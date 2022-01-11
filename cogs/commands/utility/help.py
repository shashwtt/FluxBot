import json
import os
import discord
from cogs.cog_helpers.pages import PaginatorButton, Paginator
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, Cog, slash_command
from discord.ui import Select, View, Button
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
		if os.path.isdir(f"cogs/commands/{cog}"):
			if cog != "owner" and cog != "__pycache__":
				if len(os.listdir(f"cogs/commands/{cog}")) != 0:
					cogs.append(cog)
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

	def get_all_command(self):
		aliases = {}
		for command in self.client.commands:
			aliases[f'{command}'] = str(command)
			for i in command.aliases:
				aliases[f'{i}'] = str(command)
		return aliases

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
		prefix = get_prefix(ctx.guild.id)
		working_cogs = get_working_cogs()

		if command_name.lower() in self.get_all_command():
			command_name = self.get_all_command()[f"{command_name}"]
			command = discord.utils.get(self.client.commands, name=command_name)
			await self.cmd_help(ctx, command)
			return

		# A custom url for when a user clicks on a command
		url = "https://news.rr.nihalnavath.com/posts/Help%20-%20Flux%20Commands-1fc8455b"

		all_page_description = f'**Available command Categories -**\n\n'
		for x in working_cogs:
			all_page_description = all_page_description + f"● **{x.capitalize()}**\n"
		all_page_description += "\n Select command category below for more details.."

		all_page = discord.Embed(
			description=all_page_description,
			color=0xf2cb7d,
		)

		async def my_select_view_timeout():
			my_select.disabled = True
			await message.edit(view=my_select_view)

		my_select_view = View(timeout=20)
		my_select_view.on_timeout = my_select_view_timeout
		select_options = {
			"x": "All Commands"
		}

		for i in range(len(working_cogs)):
			select_options[str(i)] = working_cogs[i]

		def index_commands(value):
			command_list = []
			for cmd_name in os.listdir(f"cogs/commands/{value.lower()}/"):
				if cmd_name.endswith(".py"):
					cmd = self.client.get_command(name=cmd_name[:-3])
					if cmd is None:
						continue
					cmd_help = cmd.help
					if cmd_help is None:
						cmd_help = "No help text provided by developer.."
					command_list.append([str(cmd), cmd_help])
			return command_list

		async def paginate(ctx, commands_, value):

			paginator_pages = []
			index = 0
			while True:
				description = ''
				for z in range(0, 7):
					try:
						description = description + f"\n **[{commands_[index][0]}]({url})**\n<:reply:928546470662119444>{commands_[index][1]}"
						index += 1
					except IndexError:
						break
				try:
					__tempvar = commands_[index]
					page = discord.Embed(title=f"{value.capitalize()} commands -", description=description)
					paginator_pages.append(page)
				except IndexError:
					page = discord.Embed(title=f"{value.capitalize()} commands -", description=description)
					paginator_pages.append(page)
					break

			paginator = Paginator(
				pages=paginator_pages,
				show_disabled=True,
				show_indicator=True,
				disable_on_timeout=True,
				timeout=18,
				custom_view=my_select_view
			)
			paginator.customize_button(
				"prev",
				button_emoji="<:left:930372441249808415>",
				button_style=discord.ButtonStyle.primary
			)
			paginator.customize_button(
				"next",
				button_emoji="<:right:930372441220472863>",
				button_style=discord.ButtonStyle.primary
			)

			await paginator.edit(ctx, message=message)

		async def my_select_callback(interaction):
			value_index = my_select.values[0]
			value = select_options[str(value_index)].lower()

			my_select.placeholder = value.capitalize()
			if my_select.values[0] == 'x':
				await interaction.message.edit(embed=all_page, view=my_select_view)
				return

			command_list = index_commands(value)

			if len(command_list) > 7:
				await paginate(ctx, command_list, value)
			else:
				description = ''
				for x in range(len(command_list)):
					description = description + f"\n **[{command_list[x][0]}]({url})**\n<:reply:928546470662119444>{command_list[x][1]}"

				page = discord.Embed(title=f"{value.capitalize()} commands -", description=description)
				await interaction.message.edit(embed=page, view=my_select_view)

		my_select = Select(
			min_values=1,
			max_values=1,
			placeholder="Select Command Category"
		)

		for i in select_options.keys():
			my_select.add_option(label=select_options[i].capitalize(), value=str(i))

		my_select.callback = my_select_callback
		my_select_view.add_item(my_select)

		if command_name == "" or command_name is None:
			message = await ctx.send(embed=all_page, view=my_select_view)
		elif command_name.lower() in working_cogs:
			my_select_view.placeholder = f"{command_name.capitalize()}"
			category_cmd_list = index_commands(command_name.lower())
			des = ''
			for x in range(len(category_cmd_list)):
				des = des + f"\n **[{category_cmd_list[x][0]}]({url})**\n<:reply:928546470662119444>{category_cmd_list[x][1]}"
			page = discord.Embed(title=f"{command_name.capitalize()} commands -", description=des)
			message = await ctx.send(embed=page, view=my_select_view)
		elif len(command_name) > 0 and command_name.lower() not in self.get_all_command():
			message = await ctx.send(embed=all_page, view=my_select_view)


# async def help(self, ctx, *, command_name=''):
# 	"""
# 	List all commands!
# 	"""
# 	prefix = get_prefix(ctx.guild.id)
# 	command_categories = []
# 	for cog in working_cogs:
# 		command_categories.append(cog.capitalize())
#
# 	if command_name == "" or command_name is None:
# 		embed = discord.Embed(
# 			title="Help",
# 			description="Help on available commands..",
# 			color=0xf2cb7d,
# 		)
# 		embed.set_footer(text=f"Use {prefix}help <category> for more info")
# 		for cog in working_cogs:
# 			if await check_field(ctx, cog, self.client):
# 				commands = []
# 				help_text = ""
# 				for command in os.listdir(f"cogs/commands/{cog}"):
# 					if not command.endswith(".py"):
# 						continue
# 					command = command[:-3]
# 					commands.append(command)
# 				for command_list_str in commands:
# 					if command_list_str == "__pycache__":
# 						continue
# 					help_text = help_text + f"`{command_list_str}`, "
# 				embed.add_field(
# 					name=cog.capitalize(),
# 					value=help_text[:-2],
# 					inline=False
# 				)
#
# 		await ctx.send(f"{command_name}", embed=embed)
# 	elif command_name.startswith("<@") and command_name.endswith(">"):
# 		embed = discord.Embed(
# 			title="Bro, are you okay?",
# 			description="You are supposed to search for command here,\n mentioning someone doesn't make any sense!!"
# 		)
# 		await ctx.message.reply(embed=embed)
# 	elif command_name in command_categories:
# 		ctx.send(embed=discord.Embed(title="whoops"))
# 	else:
#
# 		if command_name in self.aliases:
# 			command_name = self.aliases[f"{command_name}"]
# 		else:
# 			embed = discord.Embed(
# 				title="Whoops!",
# 				description=f"I cannot find any command named `{command_name}`",
# 				color=0xff3344
# 			)
# 			await ctx.send(embed=embed)
# 			return
#
# 		command = discord.utils.get(self.client.commands, name=command_name)
# 		await self.cmd_help(ctx, command)


def setup(client):
	client.add_cog(Help(client))
