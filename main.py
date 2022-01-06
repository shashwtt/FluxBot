import json
import sys

from db import *
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

"""
+------------------------------------------------+
| Defining some useful functions and variables.. |
+------------------------------------------------+
"""


class Logger(object):
    def __init__(self, filename="log.txt"):
        self.terminal = sys.stdout
        if not os.path.exists(filename):
            foil = open(filename, "w+")
            foil.close()
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        # this flush method is needed for python 3 compatibility.
        # this handles the flush command by doing nothing.
        # you might want to specify some extra behavior here.
        pass


# to keep logging output to a file
sys.stdout = Logger(filename="output.log")


async def create_prefix(guild):
    for channel in guild.text_channels:
        if guild.me.guild_permissions.send_messages and guild.me.guild_permissions.embed_links:
            em = discord.Embed(
                title='Hey there!',
                description=f'Thanks for inviting me to your server.\nMy prefix is \'`{prefix}`\' If you '
                            f'wish to change it, use the prefix command.',
                color=0x60FF60
            )
            em.add_field(
                name='Example usage:',
                value=f'<@899263193568936028>` prefix <new-prefix>`\nor\n`{prefix}prefix <new-prefix>`'
            )
            await channel.send(embed=em)
            break
    db.execute(f"INSERT INTO Prefix(guild, prefix) VALUES ('{guild.id}','{prefix}')")
    db.execute(f"INSERT INTO AutoMod(guild, _status) VALUES ('{guild.id}','enabled')")
    print(f"Created config for new server -> {str(guild)}, ID -> {guild.id}")
    conn.commit()


def get_prefix(_client, message):
    """
    Function to get prefix for a guild
    """
    try:
        fe = open('prefix.json', 'r')
        cache = json.load(fe)

        guild = str(message.guild.id)
        if guild in cache:
            # We don't want to call the database every single time
            prefix = commands.when_mentioned_or(cache[guild])(_client, message)
            return prefix

        else:
            db.execute(f"SELECT prefix FROM Prefix WHERE guild = '{str(message.guild.id)}'")
            prefix = db.fetchone()
            cache[str(guild)] = prefix[0]
            # So that it gets stored in the cache
            with open('prefix.json', 'w') as f:
                json.dump(cache, f, indent=4)

            return commands.when_mentioned_or(prefix[0])(_client, message)
    except TypeError:
        create_prefix(message.guild)


def get_config():
    if not os.path.isfile("config.json"):
        # sys.exit("'config.json' not found! Please add it and try again.")
        print("FEK")
    else:
        with open("config.json") as file:
            return json.load(file)


def load_commands():
    blacklisted_cogs = ["__pycache__"]
    blacklisted_commands = []
    print("---------------------------------")
    for folder in os.listdir("cogs/commands/"):
        if os.path.isdir(f"cogs/commands/{folder}"):
            if folder in blacklisted_cogs:
                print(f"--X Skipped Command Cog : {folder}")
                continue
            for command in os.listdir(f"cogs/commands/{folder}"):
                if command.endswith(".py"):
                    cmd = command[:-3]
                else:
                    continue
                if cmd in blacklisted_commands:
                    print(f"--X Skipped Command : {cmd}")
                    pass
                else:
                    try:
                        bot.load_extension(f"cogs.commands.{folder}.{cmd}")
                        print(f"--> Loaded command : '{cmd}'")
                    except discord.ext.commands.ExtensionAlreadyLoaded:
                        print("---------------------------------")
                        continue
                    except Exception as e:
                        exception = f"{type(e).__name__}: {e}"
                        print(f"--------------------------------------")
                        print(f"Failed to load Command : {cmd} from Cog {folder}..\n Traceback - {exception}")


def load_events():
    print("---------------------------------")
    for file in os.listdir("cogs/events/"):
        if file.endswith(".py"):
            extension = file[:-3]
            # blacklisted_ext = []
            blacklisted_ext = ["on_command_error"]
            if extension in blacklisted_ext:
                print(f"Skipped event : {extension}")
            else:
                try:
                    bot.load_extension(f"cogs.events.{extension}")
                    print(f"Loaded event  : {extension}")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    print(f"Failed to load event {extension}\n	{exception}")


load_dotenv()
TOKEN = os.getenv("TOKEN")
intents = discord.Intents.default()
intents.members = True
config = get_config()

"""
+--------------------------------+
| Making the commands.Bot object |
+--------------------------------+
"""

bot = commands.Bot(
    command_prefix=get_prefix,
    intents=intents,
    case_insensitive=True,
    allowed_mentions=discord.AllowedMentions(everyone=False),
    owner_ids=['663675391592103936']
)

# Removes the default help command of discord.py to be able to create our custom help command.
bot.remove_command("help")

# Code only run when the file is executed itself
if __name__ == '__main__':
    load_events()
    load_commands()
    if not os.path.isfile("config.json"):
        sys.exit("'config.json' not found! Please add it and try again.")
    else:
        with open("config.json") as file:
            config = json.load(file)
    prefix = config["bot_prefix"]


# The code in this event is executed every time a command has been *successfully* executed
@bot.event
async def on_command_completion(ctx):
    fullCommandName = ctx.command.qualified_name
    split = fullCommandName.split(" ")
    executedCommand = str(split[0])
    logMessage = "Executed " + str(executedCommand) + " command in " + str(ctx.guild.name) + " (ID: " + str(
        ctx.message.guild.id) + ") by " + str(ctx.message.author) + " (ID: " + str(ctx.message.author.id) + ")"
    print(logMessage)


# Run the bot with the token
bot.run(TOKEN)
