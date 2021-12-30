import discord
import hex_colors
import json

from db import *
from discord.ext import commands


class StarboardEvent(commands.Cog):
	def __init__(self, client):
		self.client = client

	async def get_star_channel(self, guild):
		with open('starboard.json', 'r') as f:
			cache = json.load(f)

		if str(guild) not in cache:
			cache[str(guild)] = {}
			db.execute(f"SELECT _channel FROM Starboard WHERE guild = '{guild}'")
			channel = await get_data(db=db)
			cache[str(guild)]['channel'] = int(channel)  # So it gets stored in the cache
			cache[str(guild)]['status'] = 'enabled'

			with open('starboard.json', 'w') as g:
				json.dump(cache, g)

			return channel
		else:
			return cache[str(guild)]['channel']

	async def get_star_guild_status(self, guild):
		with open('starboard.json', 'r') as f:
			cache = json.load(f)

		if str(guild) not in cache:
			db.execute(f"SELECT _status FROM Starboard WHERE guild = '{guild}'")
			status = await get_data(db=db)
			db.execute(f"SELECT _channel FROM Starboard WHERE guild = '{guild}'")
			channel = await get_data(db=db)

			cache[str(guild)] = {}
			cache[str(guild)]['channel'] = channel
			cache[str(guild)]['status'] = status

			with open('starboard.json', 'w') as g:
				json.dump(cache, g)
		else:
			status = cache[str(guild)]['status']

		return status

	starcount = {}  # Dictionary to keep track of the number of reactions on a message
	error = []  # List to keep track of who tried to re-star a message

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if payload.emoji.name == '⭐':
			channel = await self.get_star_channel(payload.guild_id)
			channel = int(channel)

			if channel is None:
				return

			channel = self.client.get_channel(channel)
			status = await self.get_star_guild_status(payload.guild_id)

			if status == 'enabled':
				msg_channel = self.client.get_channel(payload.channel_id)
				msg = await msg_channel.fetch_message(payload.message_id)
				user = self.client.get_user(payload.user_id)

				if not payload.member.guild_permissions.manage_messages:  # If the member doesn't have manage_messages permission
					if user.id not in self.error:
						await msg_channel.send(
							f"{user.mention}, You need `Manage Messages` permission to star messages", delete_after=10)
						self.error.append(user.id)  # So that they can't make the bot spam
						return
					return

				desc = msg.content
				if msg.content == '':
					desc = 'Attachment'

				em = discord.Embed(
					description=desc,
					color=hex_colors.l_yellow,
					timestamp=msg.created_at
				)
				em.set_author(
					name=msg.author,
					icon_url=msg.author.avatar.url)

				em.set_footer(text=f"Starred by {user}", icon_url=user.avatar.url)

				if len(msg.attachments) > 0:
					em.set_image(url=msg.attachments[0].url)

				em.add_field(
					name=f"Source",
					value=f"[Jump to message]({msg.jump_url})")

				starcount = self.starcount

				# Only the first reaction should star the message
				if str(payload.message_id) in starcount:
					starcount[str(payload.message_id)] += 1

				if not str(payload.message_id) in starcount:
					starcount[str(payload.message_id)] = 1

				if starcount[str(payload.message_id)] <= 1:
					starred = await channel.send(embed=em)
					await starred.add_reaction("⭐")

				if starcount[str(payload.message_id)] > 1:
					return


def setup(client):
	client.add_cog(StarboardEvent(client))