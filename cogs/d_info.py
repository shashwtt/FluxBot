import json
import os
import sys
import platform

import discord
from discord.ext import commands

import db


def get_prefix(_client, message):
    """
    Function to get prefix for a guild
    """
    fe = open('prefix.json', 'r')
    cache = json.load(fe)

    guild = str(message.guild.id)
    if guild in cache:
        # We don't want to call the database every single time
        prefix = commands.when_mentioned_or(cache[guild])(_client, message)
        return prefix

    else:
        db.execute(f"SELECT prefix FROM Prefix WHERE guild = '{str(message.guild.id)}'")
        prefix = db.fetchone()
        cache[str(guild)] = prefix[0]
        # So that it gets stored in the cache
        with open('prefix.json', 'w') as f:
            json.dump(cache, f, indent=4)

        return commands.when_mentioned_or(prefix[0])(_client, message)


class Info(commands.Cog, name="info"):
    def __init__(self, bot):
        self.bot = bot



    @commands.command(name="serverinfo", aliases=["si", "guild"])
    async def serverinfo(self, context):
        """
		Get information about the server.
		"""
        server = context.message.guild
        roles = [x.id for x in server.roles]
        role_length = len(roles)
        if role_length > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
        rols = ''
        for roole in range(len(roles) - 1, -1, -1):
            rols = rols + "<@&" + str(roles[roole]) + ">, "
        channels = len(server.channels)
        time = str(server.created_at)
        time = time.split(" ")
        time = time[0]

        embed = discord.Embed(
            title="**Server Name:**",
            description=f"{server}",
            color=0x42F56C
        )
        embed.set_thumbnail(
            url=server.icon_url
        )
        embed.add_field(
            name="Owner",
            value=f"<@{context.guild.owner_id}>"
        )
        embed.add_field(
            name="Server ID",
            value=server.id
        )
        embed.add_field(
            name="Member Count",
            value=server.member_count
        )
        embed.add_field(
            name="Text/Voice Channels",
            value=f"{channels}"
        )
        embed.add_field(
            name=f"Roles ({role_length})",
            value=rols
        )
        embed.set_footer(
            text=f"Created at: {time}"
        )
        await context.send(embed=embed)





def setup(bot):
    bot.add_cog(Info(bot))
