# import json
# import os
# import sys
# import discord
# from discord.enums import AuditLogAction
# from discord.ext import commands
# from discord.ext.commands import BucketType

# command_categories = ["help", "moderation", "fun"]
# intervals = (
# 	('weeks', 604800),  # 60 * 60 * 24 * 7
# 	('days', 86400),	# 60 * 60 * 24
# 	('hours', 3600),	# 60 * 60
# 	('minutes', 60),
# 	('seconds', 1),
# 	)

# def display_time(seconds, granularity=2):
# 	result = []

# 	for name, count in intervals:
# 		value = seconds // count
# 		if value:
# 			seconds -= value * count
# 			if value == 1:
# 				name = name.rstrip('s')
# 			result.append("{} {}".format(value, name))
# 	return ', '.join(result[:granularity])

# async def get_help_plis(ctx, command_name, bot_prefix, bot):
	

# async def get_command_help(ctx, command_name, bot_prefix, bot):
# 	the_data = open("command_data.json")
# 	command_is = False
# 	cmd_data = json.load(the_data)
# 	for cog_name in command_categories:
# 		for command in cmd_data[cog_name].keys():
# 			if command == command_name:
# 				command_is = True
# 				category = cog_name
# 				command_naam = command
# 				command_syntax = str(bot_prefix) + str(cmd_data[cog_name][command]["syntax"])
# 				command_interval = cmd_data[cog_name][command]["countdown"]
# 				if command_interval >= 60 :
# 					command_interval = display_time(command_interval, 1)
# 				else :
# 					command_interval = str(command_interval) + " seconds"
# 				command_description = cmd_data[cog_name][command]["description"]
# 				all_command_aliases = cmd_data[cog_name][command]["aliases"]
# 				all_command_aliases.append(command)
# 				command_aliases = ''
# 				for ca in all_command_aliases:
# 					command_aliases = str(command_aliases) + str(ca) + ", "
# 				command_aliases = command_aliases[:-2]
# 				embed=discord.Embed(title=f"`{str(bot_prefix)}{command_name}`", description=f"{command_description}", color=0x7ab3d6)
# 				embed.add_field(name="Syntax - ", value=f"`{command_syntax}`", inline=False)
# 				embed.add_field(name="Cooldown - ", value=f"`{command_interval}`", inline=True)
# 				embed.add_field(name="Aliases - ", value=f"`{command_aliases}`", inline=True)			
# 				embed.set_footer(text=f"Command Category - {category}")
# 				await ctx.send(embed=embed)
	
# 	if command_is == False:
# 		embed = discord.Embed(	
# 			title="Error!",
# 			description=f"No command named \"{command_name}\" found!",
# 			color=0xE02B2B
# 			)
# 		await ctx.send(embed=embed)