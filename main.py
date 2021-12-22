import asyncio
import json
import traceback
import os
import platform
import random
import sys

from hex_colors import colors as hex_colors
from keep_alive import keep_alive
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot

TOKEN = os.getenv("TOKEN")

keep_alive()

if not os.path.isfile("config.json"):
	sys.exit("'config.json' not found! Please add it and try again.")
else:
	with open("config.json") as file:
		config = json.load(file)



intents = discord.Intents.default()

bot = Bot(command_prefix=config["bot_prefix"], intents=intents)


# The code in this even is executed when the bot is ready
@bot.event
async def on_ready():
	print(f"Logged in as {bot.user.name}")
	print(f"Discord.py API version: {discord.__version__}")
	print(f"Python version: {platform.python_version()}")
	print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
	print("-------------------")
	status_task.start()


# Setup the game status task of the bot
@tasks.loop(seconds=5)
async def status_task():
	# statuses = ["with you!", "with Toys!", f"{config['bot_prefix']}help", "with humans!"]
	statuses = [".help"]
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=random.choice(statuses)))


# Removes the default help command of discord.py to be able to create our custom help command.
bot.remove_command("help")

if __name__ == "__main__":
	for file in os.listdir("./cogs"):
		if file.endswith(".py"):
			extension = file[:-3]
			blacklisted_ext = []
			if extension in blacklisted_ext :
				print(f"Skipped extension : {extension}")
			else:
				try:
					bot.load_extension(f"cogs.{extension}")
					print(f"Loaded extension '{extension}'")
				except Exception as e:
					exception = f"{type(e).__name__}: {e}"
					print(f"Failed to load extension {extension}\n	{exception}")


# The code in this event is executed every time someone sends a message, with or without the prefix
@bot.event
async def on_message(message):
	# Ignores if a command is being executed by a bot or by the bot itself
	if message.author == bot.user or message.author.bot:
		return
	await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.CommandNotFound):
        return
    raise error


# The code in this event is executed every time a command has been *successfully* executed
@bot.event
async def on_command_completion(ctx):
	fullCommandName = ctx.command.qualified_name
	split = fullCommandName.split(" ")
	executedCommand = str(split[0])
	logMessage = "Executed " + str(executedCommand) + " command in " + str(ctx.guild.name) + " (ID: " + str(ctx.message.guild.id) + ") by " + str(ctx.message.author) + " (ID: " + str(ctx.message.author.id) + ")"
	print(logMessage)


# The code in this event is executed every time a valid commands catches an error
@bot.event
async def on_command_error(context, error):
	try:
		if isinstance(error, commands.CommandOnCooldown):
			minutes, seconds = divmod(error.retry_after, 60)
			hours, minutes = divmod(minutes, 60)
			hours = hours % 24
			embed = discord.Embed(
				title="Hey, please slow down!",
				description=f"You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
				color=0xE02B2B
			)
			await context.send(embed=embed)
			return
		elif isinstance(error, commands.MissingPermissions):
			embed = discord.Embed(
				title="Error!",
				description="You are missing the permission `" + ", ".join(
					error.missing_perms) + "` to execute this command!",
				color=0xE02B2B
			)
			await context.send(embed=embed)
			return
		elif isinstance(error, commands.errors.RoleNotFound):
			embed = discord.Embed(
				title = "404 - Role not found!",
				description="pussy",
				color = random.choice(hex_colors)
			)
		elif isinstance(error, commands.MissingRequiredArgument):
			embed = discord.Embed(
				title="Error!",
				description=str(error).capitalize(),
				# We need to capitalize because the command arguments have no capital letter in the code.
				color=0xE02B2B
			)
			await context.send(embed=embed)
			return
		elif isinstance(error, commands.errors.CommandNotFound ):
			return
		elif isinstance(error, commands.errors.MissingPermissions):
			embed = discord.Embed(
				title="Error!",
				description="You are missing the permission `" + ", ".join(
					error.missing_perms) + "` to execute this command!",
				color=0xE02B2B
			)
			await context.send(embed=embed)
			return
			
		embed = discord.Embed(
			title="Error!",
			description=f"{error}",
			color=0xE02B2B
		)
		await context.send(embed=embed)
		raise error
	except Exception as otherErr:
		print("error -> ", otherErr)


# Run the bot with the token
bot.run(TOKEN)	
