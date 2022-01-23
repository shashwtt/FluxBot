import discord
import json
from db import *

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
		cur.execute(f"SELECT prefix FROM Prefix WHERE guild = '{guild}'")
		prefix = cur.fetchone()
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
		print('------------------')
		print("Time:", datetime.now(timezone('Asia/Kolkata')).strftime('%H:%M'), datetime.now(timezone('Asia/Kolkata')).strftime('%d - %m - %Y'))
		print(f"Servers: {(len(self.client.guilds))}")
		print(f"Users: {len(self.client.users)}")
		print("-------------------")

		await self.client.change_presence(
			activity=discord.Activity(
				name=f'.help | @Flux',
				type=discord.ActivityType.listening
			))


def setup(client):
	client.add_cog(onReady(client))
