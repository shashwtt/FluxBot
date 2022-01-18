import discord

from discord.ext import commands
from pytz import timezone
from datetime import datetime
from asyncio import sleep
from pypresence import Presence
import time

class onReady(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.RPC = Presence("877142422700834816")

	def get_member_count(self):
		karen = self.client.users
		return len(karen)

	@commands.Cog.listener()
	async def on_ready(self):
		print('--------------')
		print('All cogs loaded')
		# Since I host the bot on heroku, I'd like to know in the logs when the bot started/restarted in my own timezone
		print("Date:", datetime.now(timezone('Asia/Kolkata')).strftime('%d - %m - %Y'))
		print("Time:", datetime.now(timezone('Asia/Kolkata')).strftime('%H:%M'))
		print(f"Servers: {(len(self.client.guilds))}")
		print(f"Users: {self.get_member_count()}")
		print("-------------------")

		self.RPC.connect()
		print(self.RPC.update(
			state="Flux",
			details="Multipurpose discord bot",
			large_image="flux-512x",
			small_text="Flux - discord bot",
			large_text="Flux - discord bot",
		))

		# await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{self.get_member_count()} users!"))


def setup(client):
	client.add_cog(onReady(client))
