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


class Prefix(commands.Cog):
    def __init__(self, client):
        self.client = client

    with open("config.json", 'r') as config_file:
        config = json.load(config_file)
        config_file.close()

    @commands.command(
        name='prefix',
        usage="<new_prefix>",
        aliases=['setprefix', 'changeprefix'],
        help='Change the prefix to which the bot responds',
        description=f'Change the prefix of the bot (the prefix is the character or a word put before a command, eg - `?`)... Default prefix for flux is - `{config["bot_prefix"]}` '
    )
    @commands.has_permissions(manage_guild=True)
    async def change_prefix(self, ctx, new_prefix: str = None):
        if new_prefix is None:
            ctx.send(embed=discord.Embed(
                description=f"My prefix on this server is: `{get_prefix(ctx.guild.id)} \n\n to reset the prefix - `{get_prefix(ctx.guild.id)}prefix {self.config['bot_prefiix']}",
                color=discord.Color.brand_green(),
            ))

        if len(new_prefix) > 5:  # You can change this limit as per your wish
            await ctx.send("Prefix cannot be longer than 5 characters")
            return

        else:
            cur.execute(f"UPDATE Prefix SET prefix = '{new_prefix}' WHERE guild = '{ctx.guild.id}'")
            conn.commit()

            em = discord.Embed(
                title='Prefix changed',
                description=f'New prefix: `{new_prefix}`',
                color=hex_colors.l_green
            )
            await ctx.send(embed=em)

            # Fixing cache
            with open('prefix.json', 'r') as f:
                cache = json.load(f)

            cache[str(ctx.guild.id)] = new_prefix

            with open('prefix.json', 'w') as g:
                json.dump(cache, g)


def setup(client):
    client.add_cog(Prefix(client))
