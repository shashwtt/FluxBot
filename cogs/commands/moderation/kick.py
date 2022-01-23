import discord
import hex_colors
import json
from db import *

from discord.ext import commands
from discord.ui import View, Button, Select


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


class Kick(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(
		name='kick',
		usage='<member> [reason]',
		help='Kick a member from the Server...',
		description='Kick a mentioned member from the server by the given reason. The user will get a dm notifying him about the person, reason, and the server he was kicked from. This activity is registered in the audit log'
	)
	@commands.has_permissions(kick_members=True)
	@commands.bot_has_permissions(kick_members=True)
	async def kick(self, ctx, member: discord.Member = None, *, reason="No Reason Provided.."):

		prefix = get_prefix(ctx.guild.id)
		if member is None:
			await ctx.message.reply(embed=discord.Embed(
				title="Whom do you wish to kick?",
				description="You are supposed to mention the member you want to kick..",
				colour=0xbf4753
			).add_field(name="Usage Syntax - ", value=f"```{prefix}kick [user] [reason]```"))
			return

		if member == self.client.user:  # If  the 'member' is the bot
			view = View()
			view.add_item(Button(label="Join Support Server", url="https://discord.gg/ty7CxDYTM4"))
			await ctx.send(embed=discord.Embed(
				title="Uh-oh!",
				description="I cannot leave like this, you have to remove me manually..",
				colour=0xbf4753
			).add_field(
				name="If I caused any problem,",
				value="<:reply_arrow:928546470662119444> You can DM me with details so the developers can fix me\n\n\n",
				inline=False
			).add_field(
				name="If you want to make any suggestions to me,",
				value="<:reply:928546470662119444> probably join the [Support Server](https://discord.gg/ty7CxDYTM4)\n\n\n",
				inline=False
			), view=view
			)
			return

		# If the 'member' is the person who invoked the command
		if member == ctx.author:
			await ctx.send(embed=discord.Embed(
				title="Are you okay?",
				description="Why do you want to kick yourself?"
			))
			return

		# Checking if the other person has a higher or same role
		if member.top_role.position >= ctx.author.top_role.position:
			await ctx.send(f"{member.mention} has a higher role than you. You cannot ban them")
			return

		if member.top_role.position == ctx.author.top_role.position:
			await ctx.send(f"{member.mention} has the same top role as you. You cannot ban them.")
			return

		# Checking if the other person has a higher role than the bot
		if member.top_role.position > ctx.guild.me.top_role.position:
			await ctx.send(f"{member} has a higher role than me. I can't ban them.")
			return

		if member.top_role.position == ctx.guild.me.top_role.position:
			await ctx.send(f"{member} has the same top role as me. I cannot ban them.")
			return

		# Embed to be sent to the member
		m_em = discord.Embed(color=hex_colors.m_red)
		m_em.set_author(name=f"{ctx.author} kicked you from {ctx.guild.name}", icon_url=ctx.author.avatar.url)
		m_em.set_thumbnail(url=ctx.guild.icon.url)
		m_em.add_field(name="Reason", value=reason)

		# Embed to be sent in the channel
		em = discord.Embed(color=hex_colors.m_red)
		em.set_author(name=f"{ctx.author} kicked {member}", icon_url=ctx.author.avatar.url)
		em.set_thumbnail(url=member.avatar.url)
		em.add_field(name='Reason:', value=reason)

		try:
			await member.send(embed=m_em)
		except:
			pass

		await member.ban(reason=reason)
		await ctx.send(embed=em)
		await member.unban(reason=f"Kicked by {ctx.author}")


def setup(client):
	client.add_cog(Kick(client))
