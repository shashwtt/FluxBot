import discord
from discord.ext.commands import BucketType
from discord.ext import commands


class UnNick(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(
		name='unnick',
		usage='[member]',
		aliases=['un_nick', 'remove_nick', 'remove_nickname', 'reset_nick', 'reset_nickname'],
		help='Reset nicknames!',
		description="Reset your nickname on the server. This command can also be used to reset the nickname of other members, type `.help nick` for more!"
	)
	@commands.cooldown(2, 45, BucketType.user)
	@commands.bot_has_permissions(manage_nicknames=True)
	async def unnick(self, ctx, user: discord.Member):
		if not ctx.author.guild_permissions.manage_nicknames:
			if ctx.author != user:
				ctx.reply(
					embed=discord.Embed(
						description="You cannot change the nickname of others on this server!\n\n Missing Permission - `manage_nicknames`",
						color=discord.Color.orange()
					), mention_author=False)
				return
			if not ctx.author.guild_permissions.change_nickname:
				ctx.reply(embed=discord.Embed(
					description="Unfortunately you don't have the permission to change your own nickname on this server!\n\n Missing Permission - `change_nickname`",
					color=discord.Color.orange()
				))
				return

		if user != ctx.author:

			if ctx.author.top_role.position < user. top_role.position:
				await ctx.reply(f"{user.nick} has a higher role than you. You cannot change their nickname")
				return

			if ctx.author.top_role.position == user.top_role.position:
				await ctx.reply(f"{user.nick} ranks equal to you! You cannot nickname them.")
				return

			# Checking if the other person has a higher role than the bot
			if user.top_role.position > ctx.guild.me.top_role.position:
				await ctx.reply(f"{user.nick} has a higher role than me. I can't nickname them.")
				return

			if user.top_role.position == ctx.guild.me.top_role.position:
				await ctx.reply(f"{user.nick} has the same top role as me. I cannot nickname them.")
				return

		before_nick = user.nick

		if before_nick is None:
			before_nick = user.name

		try:
			await user.edit(nick=user.name)
		except:
			await ctx.send(embed=discord.Embed(description="That person is too powerful for me to rename...", color=discord.Color.brand_red()))
			return
		embed = discord.Embed(colour=discord.Colour.yellow())
		if user == ctx.author:
			embed.description = f"**{user.name} changed his nickname!**"
		else:
			embed.description = f"**{ctx.author.mention} changed {user.name}'s nickname!**"
		embed.add_field(name="nickname before -", value=f"```{before_nick}```", inline=False)
		embed.add_field(name="nickname now -", value=f"```{user.name}```", inline=False)
		await ctx.send(embed=embed)


def setup(client):
	client.add_cog(UnNick(client))
