import discord
import hex_colors
import json

from db import *
from discord.ext import commands


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


class UnMute(commands.Cog):
	def __init__(self, client):
		self.client = client

	with open("config.json", 'r') as config_file:
		config = json.load(config_file)
		config_file.close()

	@commands.command(
		name='unmute',
		usage='<member> [reason]',
		aliases=['unstfu', 'shuton', 'unshut'],
		help='un-mute people muted earlier!',
		description=f"un-mute the people who were muted on this server! also check - `{config['bot_prefix']}help mute`"
	)
	@commands.has_permissions(manage_roles=True)
	@commands.bot_has_permissions(manage_roles=True)
	async def unmute(self, ctx, member: discord.Member, *, reason="No reason provided"):
		role = discord.utils.get(ctx.guild.roles, name='Muted')
		if role is None:
			permissions = discord.Permissions(send_messages=False)
			await ctx.send(f"<:flux_x:934693031020474368> Your server doesn't have a 'Muted' role, I highly doubt {member} is muted")
			await ctx.guild.create_role(
				name='Muted',
				permissions=permissions,
				reason='For mute command')  # Making new role

			for channel in ctx.guild.channels:  # Changing the permission for the Muted role in all channels
				try:
					overwrite = channel.overwrites_for(role)
					overwrite.send_messages = False

					await channel.set_permissions(role, overwrite=overwrite)
				except:
					break

		if role not in member.roles:
			await ctx.send(embed=discord.Embed(description=f"<:flux_x:934693031020474368> {member} is not muted, you can only unmute people who are muted"))
			return

		else:
			await member.remove_roles(role, reason=f'Unmute command ran by {ctx.author}')

			em = discord.Embed(
				description=f"<:flux_check:934693030592655411> {member.mention} was un-muted by {ctx.author}",
				color=hex_colors.l_green
			)

			await ctx.message.delete()
			await ctx.send(embed=em)


def setup(client):
	client.add_cog(UnMute(client))
