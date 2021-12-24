import json
import os
import sys
import platform

import discord
from discord.ext import commands
from cogs.cog_helpers import help

if not os.path.isfile("config.json"):
	sys.exit("'config.json' not found! Please add it and try again.")
else:
	with open("config.json") as file:
		config = json.load(file)

def checkField(user, name, message):
	presence = True
	if name == "owner":
		if user not in config['owners']:
			presence = False

	if name == 'moderation':
		if message.author.guild_permissions.administrator == False:
			presence = False
			
	return presence


class Info(commands.Cog, name="info"):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="help")
	async def help(self, context,*, command_name=''):
		"""	
		List all commands!
		"""
		prefix = config["bot_prefix"]
		if command_name == "" or command_name == None:
			if not isinstance(prefix, str):
				prefix = prefix[0]
			embed = discord.Embed(title="Help", description="List of available commands:", color=0x42F56C)
			for i in self.bot.cogs:
				fieldAdd = checkField(context.message.author.id, i, context.message)
				if fieldAdd == False:
					pass
				else:
					cog = self.bot.get_cog(i.lower())
					commands = cog.get_commands()
					command_list = [command.name for command in commands]
					help_text = ''
					for cmnd in command_list:
						help_text = help_text + f"`{cmnd}`, "
					embed.add_field(name=i.capitalize(), value=f'{help_text[:-2]}', inline=False)	
			await context.send(command_name, embed=embed)
		else :
			cmds = self.bot.commands
			for cmnd in cmds :
				name = cmnd.name
				if name == command_name:
					aliases = f"`{str(command_name)}`" + "".join(f", `{al}`" for al in cmnd.aliases)
					embed = discord.Embed(
						title=f"`{prefix}{name}`",
						description=f"{cmnd.help}",
						color=0x42F56C)
					embed.add_field(name="Aliases - ", value=f"{aliases}", inline=False)
					await context.send(embed=embed)
					return
			embed = discord.Embed(
				title = "Error 404",
				description = f"unknown command `{command_name}`",
				color=0xff3344
			)
			await context.send(embed=embed)
			# print(names)
			return

	@commands.command(name="serverinfo", aliases=["si", "guild"])
	async def serverinfo(self, context):
		"""
		Get information about the server.
		"""
		server = context.message.guild
		roles = [x.id for x in server.roles]
		role_length = len(roles)
		if role_length > 50:
			roles = roles[:50]
			roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
		rols = ''
		for roole in range(len(roles)-1, -1, -1):
			rols = rols + "<@&" + str(roles[roole]) + ">, "
		channels = len(server.channels)
		time = str(server.created_at)
		time = time.split(" ")
		time = time[0]

		embed = discord.Embed(
			title="**Server Name:**",
			description=f"{server}",
			color=0x42F56C
		)
		embed.set_thumbnail(
			url=server.icon_url
		)
		embed.add_field(
			name="Owner",
			value=f"<@{context.guild.owner_id}>"
		)
		embed.add_field(
			name="Server ID",
			value=server.id
		)
		embed.add_field(
			name="Member Count",
			value=server.member_count
		)
		embed.add_field(
			name="Text/Voice Channels",
			value=f"{channels}"
		)
		embed.add_field(
			name=f"Roles ({role_length})",
			value=rols
		)
		embed.set_footer(
			text=f"Created at: {time}"
		)
		await context.send(embed=embed)

	@commands.command(name="ping", aliases=["latency"])
	async def ping(self, context):
		"""
		Check if the bot is alive.
		"""
		embed = discord.Embed(
			title="🏓 Pong!",
			description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
			color=0x42F56C
		)
		await context.send(embed=embed)

	@commands.command(name="invite")
	async def invite(self, context):
		"""
		Get the invite link of the bot!
		"""
		embed = discord.Embed(
			description=f"Invite me by clicking [here](https://discordapp.com/oauth2/authorize?&client_id={config['application_id']}&scope=bot&permissions=470150263).",
			color=0xD75BF4
		)
		try:
			# To know what permissions to give to your bot, please see here: https://discordapi.com/permissions.html and remember to not give Administrator permissions.
			await context.author.send(embed=embed)
			await context.send("I sent you a private message!")
		except discord.Forbidden:
			await context.send(embed=embed)

	@commands.command(name="support", aliases=["supportserver"])
	async def server(self, context):
		"""
		Get invite link of bot's discord server!
		"""
		embed = discord.Embed(
			description=f"We currently don't have a support server. It will be added soon xD",
			color=0xD75BF4
		)
		try:
			await context.author.send(embed=embed)
			await context.send("I sent you a private message!")
		except discord.Forbidden:
			await context.send(embed=embed)

def setup(bot):
	bot.add_cog(Info(bot))
