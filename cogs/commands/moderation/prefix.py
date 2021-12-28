import discord
import hex_colors
import json

from db import *
from discord.ext import commands


class Prefix(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='prefix', aliases=['setprefix', 'changeprefix'],
                      help='Change the prefix to which the bot responds')
    @commands.has_permissions(manage_guild=True)
    async def change_prefix(self, ctx, new_prefix: str = None):
        if len(new_prefix) > 5:  # You can change this limit as per your wish
            await ctx.send("Prefix cannot be longer than 5 characters")
            return

        else:
            db.execute(f"UPDATE Prefix SET prefix = '{new_prefix}' WHERE guild = '{ctx.guild.id}'")
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
