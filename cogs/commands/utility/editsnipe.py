import discord
import random
import pytz
import hex_colors

from datetime import datetime
from discord.ext import commands

edit_msg = {}


class editSnipe(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        edit_msg[str(before.channel.id)] = {}

        edit_msg[str(before.channel.id)]['before'] = before.content
        edit_msg[str(before.channel.id)]['after'] = after.content
        edit_msg[str(before.channel.id)]['author'] = before.author
        edit_msg[str(before.channel.id)]['time'] = datetime.now(pytz.utc)  # This will be used for the timestamp

    @commands.command(name='editsnipe', aliases=['es'], help='Check the last edited message in the channel')
    async def editsnipe(self, ctx):
        try:
            em = discord.Embed(color=random.choice(hex_colors.colors), timestamp=edit_msg[str(ctx.channel.id)]['time'])
            em.set_author(name=f"{edit_msg[str(ctx.channel.id)]['author']} said:",
                          icon_url=edit_msg[str(ctx.channel.id)]['author'].avatar.url)
            em.add_field(name='Before', value=edit_msg[str(ctx.channel.id)]['before'],
                         inline=False)  # If the embed has 2 fields, using inline=False only once is enough)
            em.add_field(name='After', value=edit_msg[str(ctx.channel.id)]['after'])

            await ctx.send(embed=em)
        except:
            await ctx.send("There are no recently edited messages")


def setup(client):
    client.add_cog(editSnipe(client))