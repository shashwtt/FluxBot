import json
from db import *
import os
import random
import sys

from hex_colors import colors as hex_colors
from keep_alive import keep_alive
import discord
from discord.ext import commands
from dotenv import load_dotenv

"""
+------------------------------------------------+
| Defining some useful functions and variables.. |
+------------------------------------------------+
"""


def get_prefix(_client, message):
    """
    Function to get prefix for a guild
    """
    with open('prefix.json', 'r') as f:
        cache = json.load(f)

    guild = str(message.guild.id)
    if guild in cache:  # We don't want to call the database every single time
        prefix = commands.when_mentioned_or(cache[guild])(_client, message)
        return prefix

    else:
        db.execute(f"SELECT prefix FROM Prefix WHERE guild = {str(message.guild.id)}")
        prefix = db.fetchone()
        cache[guild] = prefix[0]  # So that it gets stored in the cache
        with open('prefix.json', 'w') as f:
            json.dump(cache, f)

        return commands.when_mentioned_or(prefix[0])(_client, message)


def get_config():
    if not os.path.isfile("config.json"):
        sys.exit("'config.json' not found! Please add it and try again.")
    else:
        with open("config.json") as file:
            return json.load(file)


def load_commands():
    for file in os.listdir("./cogs/commands"):
        if file.endswith("_cmd.py"):
            extension = file[:-7]
            blacklisted_ext = []
            if extension in blacklisted_ext:
                print(f"Skipped extension : {extension}")
            else:
                try:
                    bot.load_extension(f"cogs.commands.{extension}")
                    print(f"Loaded command '{extension}'")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    print(f"Failed to load extension {extension}\n	{exception}")


def load_events():
    for file in os.listdir("./cogs/events"):
        if file.endswith("_ev.py"):
            extension = file[:-6]
            blacklisted_ext = []
            if extension in blacklisted_ext:
                print(f"Skipped event : {extension}")
            else:
                try:
                    bot.load_extension(f"cogs.events.{extension}")
                    print(f"Loaded extension '{extension}'")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    print(f"Failed to load extension {extension}\n	{exception}")


load_dotenv()
TOKEN = os.getenv("TOKEN")
intents = discord.Intents.default()
keep_alive()
config = get_config()

"""
+--------------------------------+
| Making the commands.Bot object |
+--------------------------------+
"""

bot = commands.Bot(
    command_prefix=get_prefix,
    intents=discord.Intents.all(),
    case_insensitive=True,
    allowed_mentions=discord.AllowedMentions(everyone=False),
    owner_id=663675391592103936
)

# Removes the default help command of discord.py to be able to create our custom help command.
bot.remove_command("help")

if __name__ == '__main__':
    load_events()
    load_commands()


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
    logMessage = "Executed " + str(executedCommand) + " command in " + str(ctx.guild.name) + " (ID: " + str(
        ctx.message.guild.id) + ") by " + str(ctx.message.author) + " (ID: " + str(ctx.message.author.id) + ")"
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
                title="404 - Role not found!",
                description="pussy",
                color=random.choice(hex_colors)
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
        elif isinstance(error, commands.errors.CommandNotFound):
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
