import discord
import db
import json

from discord.ext import commands
from pytz import timezone
from datetime import datetime
from asyncio import sleep

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


class onReady(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		print('--------------')
		print('All cogs loaded')
		# Since I host the bot on heroku, I'd like to know in the logs when the bot started/restarted in my own timezone
		print("Date:", datetime.now(timezone('Asia/Kolkata')).strftime('%d - %m - %Y'))
		print("Time:", datetime.now(timezone('Asia/Kolkata')).strftime('%H:%M'))
		print(f"Servers: {(len(self.client.guilds))}")
		print(f"Users: {len(self.client.users)}")
		print("-------------------")

		await self.client.change_presence(
			activity=discord.Activity(
				type=discord.ActivityType.listening,
				name=f'.help',
			))

		# await self.client


def setup(client):
	client.add_cog(onReady(client))
