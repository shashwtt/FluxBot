import discord
import random
import asyncio
import hex_colors

from discord.ext import commands

class Embed(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='embed', help='Send an embed in a channel')
    @commands.has_permissions(manage_guild=True)
    async def embed(self, ctx):
        def check(message: discord.Message) -> bool:
            return message.author == ctx.author and message.channel == ctx.channel

        await ctx.send("What channel do you want the embed to be in? You have 30 seconds to respond")
        try:
            channel_name = await self.client.wait_for('message', timeout=30, check=check)

            mode = '' #the mode we will use to search for the channel, name or id
            channel_name = channel_name.content

            if channel_name.startswith('<#') and channel_name.endswith('>'):
                channel_name = channel_name.strip('<#>')
                channel_name = int(channel_name)
                mode = 'id'

            else:
                mode = 'name'

            if mode == 'id':
                channel = discord.utils.get(ctx.guild.channels, id=channel_name) #because channel_name is a message, and we want the message's content
                if channel:
                    await ctx.send('Found the channel')

                if not channel:
                    await ctx.send("I couldn't find that channel in this server. Maybe I don't have the permission to view it.")
                    return

            if mode == 'name':
                channel = discord.utils.get(ctx.guild.channels, name=channel_name) #because channel_name is a message, and we want the message's content
                if channel:
                    await ctx.send('Found the channel')

                if not channel:
                    await ctx.send("I couldn't find that channel in this server. Maybe I don't have the permission to view it.")
                    return

        except asyncio.TimeoutError:
            await ctx.send("You ran out of time")

        await ctx.send("What should be the title of the embed (Keep it less than 256 characters)? You have 30 seconds to respond.")
        try:
            embed_title = await self.client.wait_for('message', timeout=30, check=check)
            embed_title = embed_title.content
            if len(embed_title) > 256:
                await ctx.send("The title cannot be longer than 256 characters, re-run the command.")
                return
        except asyncio.TimeoutError:
            await ctx.send("You ran out of time")

        await ctx.send("What should be the description of the embed (Keep it less than 2048 characters.)? You have 5 minutes to respond.")
        try:
            embed_desc = await self.client.wait_for('message', timeout=300, check=check)
            embed_desc = embed_desc.content
            if len(embed_title) > 2048:
                await ctx.send("The description cannot be longer than 2048 characters, re-run the command.")
                return
        except asyncio.TimeoutError:
            await ctx.send("You ran out of time")

        await ctx.send("""What should be the color of the embed? These are your options:
`red`
`l_red` (light red)
`green`
`l_green` (paler green)
`d_green` (dark green)
`yellow`
`l_yellow` (light yellow)
`blue`
`l_blue` (light blue)
`cyan`
""") #The options are the colors in hex_colors
        valid_color_choices = ['red', 'l_red', 'green', 'l_green', 'd_green', 'yellow', 'l_yellow', 'blue', 'l_blue', 'cyan']
        try:
            embed_color = await self.client.wait_for('message', timeout=60, check=check)
            if embed_color.content.lower() not in valid_color_choices:
                await ctx.send("That choice is invalid")
                return

            else:
                embed_color = embed_color.content.lower() #this line doesn't matter much

        except asyncio.TimeoutError:
            await ctx.send("You ran out of time")

        em = discord.Embed(title=embed_title, description=embed_desc, color=hex_colors.get_color(embed_color)) #if you didn't write that 'else' line before, write: color = embed_color.content.lower(). If the command still doesn't work, download the new hex_colors file (i added a function)

        #If you don't want the bot to send the embed as the author, don't create the webhook
        webhooks = await channel.webhooks()
        webhook = discord.utils.get(webhooks, name='roastinator') #Enter your bot's name here

        if webhook is None:
            webhook = await channel.create_webhook(name='roastinator')

        await webhook.send(embed=em, username=ctx.author.display_name, avatar_url=ctx.author.avatar_url)


def setup(client):
    client.add_cog(Embed(client))