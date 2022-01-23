import discord
from discord.ext import commands
from asyncio import sleep
from discord.ext.commands import CommandOnCooldown, BucketType


def parse_time(time):
	x_list = time.split()
	mode = ''
	time = ''
	for x in x_list:
		if x == ' ':
			continue
		try:
			int_time = int(x)
			time += str(int_time)
		except Exception:
			mode += x

	if len(mode) > 0:
		if mode == 's' or mode == 'seconds' or mode == 'second':
			multiplier = 1
		if mode == 'm' or mode == 'minutes' or mode == 'minute' or mode == "min":
			multiplier = 60
		if mode == 'h' or mode == 'hours' or mode == 'hour' or mode == "hr":
			multiplier = 60 * 60
		if mode == 'd' or mode == 'days' or mode == 'day':
			multiplier = 60 * 60 * 24
		else:
			return False
	else:
		multiplier = 60

	try:
		total_seconds = multiplier * int(time)
		return total_seconds
	except Exception:
		return False


def clarify_time(seconds):
	seconds = int(seconds)
	if 60 > seconds > 0:
		return str(seconds) + " seconds"
	elif seconds <= 3600:
		return str(round(seconds / 60)) + " minutes"
	elif seconds <= 86400:
		return str(round(seconds / 3600)) + " hours"
	elif seconds < 86400:
		return str(round(seconds / 86400)) + " days"
	elif seconds is None or seconds == False:
		return "forever"
	else:
		return "unknown minutes"


class MuteUnmute(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(
		name='mute',
		usage='<member> [reason]',
		aliases=['stfu', 'shut', 'antispeak'],
		help='Mute people permanently or temporarily',
		description='Mute users with this command. example of time = '
	)
	@commands.has_permissions(manage_roles=True)
	@commands.bot_has_permissions(manage_roles=True)
	async def mute(self, ctx, member: discord.Member, time=None, *, reason=None):
		seconds = None
		if time is not None:
			seconds = parse_time(time)
		role = discord.utils.get(ctx.guild.roles, name='Muted')
		permissions = discord.Permissions(send_messages=False)

		if seconds is None or seconds == False:
			await ctx.reply(
				embed=discord.Embed(
					description=f"The time `{time}` is incorrect!\n\n time examples - `10`, `30s`, `2h`, `7d`"),
				mention_author=False
			)
			return

		if not role in ctx.guild.roles:
			await ctx.reply(
				"Hold on, making a 'Muted' role. Don't worry, this process won't take place every time you run this "
				"command", mention_author=False)
			await ctx.guild.create_role(
				name='Muted',
				permissions=permissions,
				reason='For mute command'
			)  # Making new role

		role = discord.utils.get(ctx.guild.roles, name='Muted')  # The old role variable might have returned None

		if role in member.roles:
			await ctx.send(
				embed=discord.Embed(description=f"<:flux_x:934693031020474368> {member.name} is already muted!"))
			return

		try:
			await member.add_roles(role, reason=f"{ctx.author} ran the mute command")
		except:
			await ctx.send(embed=discord.Embed(
				description="The 'Muted' role is above my highest role. Please fix that in the server settings and then run the mute command. Having trouble doing that? Then simply deleted the 'Muted' role."))
			return

		em = discord.Embed(
			description=f"<:flux_check:934693030592655411> {member.mention} was muted by {ctx.author} for {clarify_time(seconds)}",
			color=discord.Color.random()
		)

		if reason is not None:
			em.description = em.description + f"\n\nReason - ```{reason}```"

		await ctx.send(embed=em)

		for channel in ctx.guild.channels:  # Changing the permission for the Muted role in all channels
			try:
				overwrite = channel.overwrites_for(role)
				overwrite.send_messages = False

				await channel.set_permissions(role, overwrite=overwrite)
			except:
				await ctx.send(
					"Since I don't have the manage channels permission, I couldn't change the permissions for the "
					"muted role in the channels.")
				break

		if time is not None:
			await sleep(seconds)
			await member.remove_roles(role, reason=f"Temporary mute is over. Responsible moderator: {ctx.author}")


def setup(client):
	client.add_cog(MuteUnmute(client))
