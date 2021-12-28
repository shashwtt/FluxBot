import discord
import random
import pytz
import hex_colors

from datetime import datetime
from discord.ext import commands

del_msg = {}
edit_msg = {}


class Snipe(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        channel = str(message.channel.id)
        del_msg[channel] = {}
        del_msg[channel]['content'] = message.content
        del_msg[channel]['author'] = message.author
        del_msg[channel]['time'] = datetime.now(pytz.utc)  # This will be used for the timestamp

        if len(message.attachments) > 0:
            del_msg[channel]['attachment'] = str(message.attachments[0].url)
        else:
            del_msg[channel]['attachment'] = None

        if len(message.embeds) > 0:
            del_msg[channel]['embed'] = message.embeds[0]
        else:
            del_msg[channel]['embed'] = None

    @commands.command(name='snipe', help='Check the last deleted message in the channel')
    async def snipe(self, ctx):
        try:
            msg_content = del_msg[str(ctx.channel.id)]['content']
            if msg_content == '':  # If the message had no text, it means that it had an attachment. Since the
                # message is deleted, we can't retrieve that.
                msg_content = "There was an image or an embed in the deleted message that couldn't be loaded, " \
                              "but here's the url "

            em = discord.Embed(description=msg_content, color=random.choice(hex_colors.colors),
                               timestamp=del_msg[str(ctx.channel.id)]['time'])
            em.set_author(name=f"{del_msg[str(ctx.channel.id)]['author']} said:",
                          icon_url=del_msg[str(ctx.channel.id)]['author'].avatar_url)

            if del_msg[str(ctx.channel.id)]['attachment'] is not None:
                em.description = f"{msg_content} \n\n [**Attachment**]({del_msg[str(ctx.channel.id)]['attachment']})"

            if del_msg[str(ctx.channel.id)]['embed'] is not None:
                em.description = f"{msg_content} \n\n The deleted message had this embed:"

            await ctx.send(embed=em)

            if del_msg[str(ctx.channel.id)][
                'embed'] is not None:  # Yes, same check 2nd time. I needed it to send the embed after the main embed
                await ctx.send(embed=del_msg[str(ctx.channel.id)]['embed'])

        except discord.errors.Forbidden or discord.Forbidden:
            await ctx.send("I don't have the embed links permission. I need that.")

        except KeyError as e:
            await ctx.send("There are no recently deleted messages")


def setup(client):
    client.add_cog(Snipe(client))
