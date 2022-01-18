import random

import discord
import hex_colors
import json
from db import *

from discord.ext import commands
from discord.ui import View, Button, Select

colors = hex_colors.colors


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


class UnBan(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(name='unban', help='pardon/unban a banned member from the server!', usage='<member> <reason>')
	@commands.has_permissions(ban_members=True)
	@commands.bot_has_permissions(ban_members=True)
	async def unban(self, ctx, member: discord.Member, *, reason="No reason provided"):
		try:
			banned = await member.guild.fetch_ban(member)
		except discord.NotFound:
			banned = False
			lol_em_list = [
				"Bruh, you are trying to unban someone who is not even banned, lol!",
				"Cannot unban a member who is not even banned",
				f"Rumors say that {member.mention} was never banned!"
			]
			lol_em = discord.Embed(
				description=random.choice(lol_em_list),
				colour=discord.Colour.orange(),
			)
			return await ctx.send(embed=lol_em)

		# Embed to be sent to the member
		m_em = discord.Embed(color=hex_colors.m_red, description=f"You were unbanned by {ctx.author.name}#{ctx.author.discriminator} from {ctx.guild.name}")
		m_em.set_thumbnail(url=ctx.guild.icon.url)
		m_em.add_field(name="Reason", value=reason)

		# Embed to be sent in the channel
		em = discord.Embed(color=hex_colors.m_red)
		em.set_author(name=f"{member} was unbanned by {ctx.author}!", icon_url=ctx.author.avatar.url)
		em.set_thumbnail(url=member.avatar.url)
		em.add_field(name='Reason:', value=reason)

		try:
			await member.send(embed=m_em)
		except:
			pass

		await member.unban(reason=reason)
		await ctx.send(embed=em)


def setup(client):
	client.add_cog(UnBan(client))
