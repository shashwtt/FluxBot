import discord
from discord.ext.commands import BucketType
from discord.ext import commands


class Nick(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.cooldown(2, 45, BucketType.user)
	@commands.bot_has_permissions(manage_nicknames=True)
	@commands.command(name='nick', aliases=['nickname', 'name'], help='Manage your and other\'s nicknames')
	async def nick(self, ctx, user: discord.Member, *, nickname):
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

		if len(nickname) > 32:
			embed_err = discord.Embed(
				description="A nickname cannot be longer than 32 digits...",
				colour=discord.Colour.brand_red()
			)
			embed_err.set_footer(text="Choose a shorter nickname!")
			await ctx.message.reply(embed=embed_err)
			return
		try:
			await user.edit(nick=nickname)
		except:
			await ctx.send(embed=discord.Embed(description="That person is too powerful for me to rename...", color=discord.Color.brand_red()))
			return
		embed = discord.Embed(colour=discord.Colour.yellow())
		if user == ctx.author:
			embed.description = f"**{user.name} changed his nickname!**"
		else:
			embed.description = f"**{ctx.author.mention} changed {user.name}'s nickname!**"
		embed.add_field(name="nickname before -", value=f"```{before_nick}```", inline=False)
		embed.add_field(name="nickname now -", value=f"```{nickname}```", inline=False)
		await ctx.send(embed=embed)


def setup(client):
	client.add_cog(Nick(client))
