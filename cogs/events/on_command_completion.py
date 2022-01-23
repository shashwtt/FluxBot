# The code in this event is executed every time a command has been *successfully* executed

from discord.ext import commands
from db import *
import sys
import json


class OnCommandCompletion(commands.Cog):
	def __init__(self, client):
		self.client = client
		if not os.path.isfile("config.json"):
			sys.exit("'config.json' not found! Please add it and try again.")
		else:
			with open("config.json") as file:
				self.config = json.load(file)
		self.prefix = self.config["bot_prefix"]

	@commands.Cog.listener()
	async def on_command_completion(self, ctx):
		fullCommandName = ctx.command.qualified_name
		split = fullCommandName.split(" ")
		executedCommand = str(split[0])
		logMessage = "Executed " + str(executedCommand) + " command in " + str(ctx.guild.name) + " (ID: " + str(
			ctx.message.guild.id) + ") by " + str(ctx.message.author) + " (ID: " + str(ctx.message.author.id) + ")"
		print(logMessage)


def setup(client):
	client.add_cog(OnCommandCompletion(client))
