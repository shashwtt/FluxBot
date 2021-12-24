import discord
import random
import pytz
import hex_colors

from datetime import datetime
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

edit_msg = {}
del_msg = {}

class general(commands.Cog, name="general"):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message_edit(self, before, after):
		edit_msg[str(before.channel.id)] = {}

		edit_msg[str(before.channel.id)]['before'] = before.content
		edit_msg[str(before.channel.id)]['after'] = after.content
		edit_msg[str(before.channel.id)]['author'] = before.author
		edit_msg[str(before.channel.id)]['time'] = datetime.now(pytz.utc) #This will be used for the timestamp

	@commands.Cog.listener()
	async def on_message_delete(self, message):
		channel = str(message.channel.id)
		del_msg[channel] = {}
		del_msg[channel]['content'] = message.content
		del_msg[channel]['author'] = message.author
		del_msg[channel]['time'] = datetime.now(pytz.utc) #This will be used for the timestamp

		if len(message.attachments) > 0:
			del_msg[channel]['attachment'] = str(message.attachments[0].url)
		else:
			del_msg[channel]['attachment'] = None

		if len(message.embeds) > 0:
			del_msg[channel]['embed'] = message.embeds[0]
		else:
			del_msg[channel]['embed'] = None


	@commands.command(
		name='snipe', 
		help='Check the last deleted message in the channel',
		brief='snipe')
	async def snipe(self, ctx):
		try:
			msg_content = del_msg[str(ctx.channel.id)]['content']
			if msg_content == '': #If the message had no text, it means that it had an attachment. Since the message is deleted, we can't retrieve that.
				msg_content = "There was an image or an embed in the deleted message that couldn't be loaded, but here's the url"


			em = discord.Embed(description=msg_content, color=random.choice(hex_colors.colors), timestamp=del_msg[str(ctx.channel.id)]['time'])
			em.set_author(name=f"{del_msg[str(ctx.channel.id)]['author']} said:", icon_url=del_msg[str(ctx.channel.id)]['author'].avatar_url)

			if del_msg[str(ctx.channel.id)]['attachment'] is not None:
				em.description = f"{msg_content} \n\n [**Attachment**]({del_msg[str(ctx.channel.id)]['attachment']})"

			if del_msg[str(ctx.channel.id)]['embed'] is not None:
				em.description = f"{msg_content} \n\n The deleted message had this embed:"

			await ctx.send(embed=em)

			if del_msg[str(ctx.channel.id)]['embed'] is not None:  # Yes, same check 2nd time. I needed it to send the embed after the main embed
				await ctx.send(embed=del_msg[str(ctx.channel.id)]['embed'])

		except discord.errors.Forbidden or discord.Forbidden:
			await ctx.send("I don't have the embed links permission. I need that.")

		except KeyError as e:
			print(e)
			await ctx.send("There are no recently deleted messages")


	@commands.command(
		name='editsnipe', 
		aliases=['es'], 
		help='Check the last edited message in the channel',
		brief='editsnipe')
	async def editsnipe(self, ctx):
		try:
			em = discord.Embed(color=random.choice(hex_colors.colors), timestamp=edit_msg[str(ctx.channel.id)]['time'])
			em.set_author(name=f"{edit_msg[str(ctx.channel.id)]['author']} said:", icon_url=edit_msg[str(ctx.channel.id)]['author'].avatar_url)
			em.add_field(name='Before', value=edit_msg[str(ctx.channel.id)]['before'], inline=False) #If the embed has 2 fields, using inline=False only once is enough)
			em.add_field(name='After', value=edit_msg[str(ctx.channel.id)]['after'])

			await ctx.send(embed=em)
		except:
			await ctx.send("There are no recently edited messages")

	@commands.command(
		name='roleinfo', 
		aliases=['ri'], 
		help='Shows information about a role',
		brief='ri <role>')
	@cooldown(1, 5, BucketType.user)
	async def role_info(self, ctx, role:discord.Role):
		if role not in ctx.guild.roles:
			await ctx.send("I can't find that role in this server..")
			return

		perms = role.permissions #returns a list of permissions

		d_perms = '' #d stands for decorated

		for perm in perms: #Rewriting the perms in a more presentable manner
			if not False in perm: #We only want to log the permissions that the role has
				perm = str(perm)
				if '_' in perm:
					perm = perm.replace('_',' ')
				if 'guild' in perm:
					perm = perm.replace('guild','server') #Since guilds are called servers in the GUI
				if '(' in perm:
					perm = perm.replace("('",'')
					perm = perm.replace("'",'')
					perm = perm.replace(')','')
					perm = perm.replace(',',' ')

				perm = perm.title() #Capitalizing first letter of every word
				perm = perm.replace('True','')
				d_perms += f"{perm}\n"


		em = discord.Embed(title='@'+role.name, color=role.color) #I chose role.color, but that's a personal preference
		em.add_field(name='ID', value=role.id, inline=False)
		em.add_field(name="Permissions", value=d_perms, inline=False)
		em.add_field(name='Number of people that have this role', value=len(role.members), inline=False)
		em.add_field(name='Can everyone mention this role?', value=bool_str(role.mentionable), inline=False)

		await ctx.send(embed=em)

def bool_str(variable):
	if variable == True:
		return 'Yes'
	if variable == False:
		return 'No'

def setup(bot):
	bot.add_cog(general(bot))