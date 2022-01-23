import discord

from discord.ext import commands
from db import *
import sys
import json


class OnGuildJoin(commands.Cog):
    def __init__(self, client):
        self.client = client
        if not os.path.isfile("config.json"):
            sys.exit("'config.json' not found! Please add it and try again.")
        else:
            with open("config.json") as file:
                self.config = json.load(file)
        self.prefix = self.config["bot_prefix"]

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        for channel in guild.text_channels:
            if guild.me.guild_permissions.send_messages and guild.me.guild_permissions.embed_links:
                em = discord.Embed(
                    title='Hey there!',
                    description=f'Thanks for inviting me to your server.\nMy prefix is \'`{self.prefix}`\' If you '
                                f'wish to change it, use the prefix command.',
                    color=0x60FF60
                )
                em.add_field(
                    name='Example usage:',
                    value=f'{self.client.user.mention}` prefix <new-prefix>`\nor\n`{self.prefix}prefix <new-prefix>`'
                )
                await channel.send(embed=em)
                break
        cur.execute(f"INSERT INTO Prefix(guild, prefix) VALUES ('{guild.id}','{self.prefix}')")
        cur.execute(f"INSERT INTO AutoMod(guild, _status) VALUES ('{guild.id}','enabled')")
        print(f"Created config for new server -> {str(guild)}, ID -> {guild.id}")
        conn.commit()


def setup(client):
    client.add_cog(OnGuildJoin(client))
