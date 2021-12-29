import discord
import hex_colors
import json

from db import *
from discord.ext import commands


class StarboardCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(name='starboard', help='Configure the starboard for your serverr', invoke_without_command=True)
    @commands.has_permissions(manage_messages=True)
    async def starboard_commands(self, ctx):
        guild = str(ctx.guild.id)
        with open('starboard.json', 'r') as f:
            cache = json.load(f)
        em = discord.Embed(
            title="Starboard Commands",
            description="""
`channel` - Set the starboard channel
`enable`  - Enable starboard for the server
`disable` - Disable starboard for the server
            """,
            color=hex_colors.l_yellow)
        channel = None
        if guild not in cache:
            db.execute(f"SELECT _status FROM Starboard WHERE guild = '{ctx.guild.id}'")
            status = await get_data(db=db)
            cache[guild] = {}

            if status == 'enabled':
                db.execute(f"SELECT _channel FROM Starboard WHERE guild = '{ctx.guild.id}'")
                channel = await get_data(db=db)
                cache[guild]['status'] = 'enabled'
                cache[guild]['channel'] = str(channel)
            else:
                em.set_footer(text="Starboard hasn't been setup in this server yet")

        else:
            channel = cache[guild]['channel']

        em.add_field(
            name='Starboard channel:',
            value=f'<#{channel}>'
        )

        await ctx.send(embed=em)

    @starboard_commands.command(name='channel', help="Set the starboard channel")
    async def channel(self, ctx, channel: discord.TextChannel):
        guild = str(ctx.guild.id)
        with open('starboard.json', 'r') as f:
            cache = json.load(f)

        try:
            db.execute(f"INSERT INTO Starboard(guild, _channel, _status) VALUES ('{ctx.guild.id}','{channel.id}','enabled')")
        except:
            db.execute(f"UPDATE Starboard SET _channel = '{channel.id}' WHERE guild = '{ctx.guild.id}'")

        if guild not in cache:
            cache[guild] = {}
            cache[guild]['status'] = 'enabled'
            cache[guild]['channel'] = str(channel.id)
        else:
            cache[guild]['status'] = 'enabled'
            cache[guild]['channel'] = str(channel.id)

        conn.commit()
        await ctx.send(f"Starboard set to <#{channel.id}>")

        with open('starboard.json', 'w') as g:
            json.dump(cache, g)


    @starboard_commands.command(name='disable', help="Disable starboard")
    async def disable_starboard(self, ctx):
        guild = str(ctx.guild.id)
        with open('starboard.json', 'r') as f:
            cache = json.load(f)


        try:
            db.execute(f"UPDATE Starboard SET _status = 'disabled' WHERE guild = '{ctx.guild}'")
            conn.commit()
            await ctx.send("Disabled starboard")

            if guild not in cache:
                cache[guild] = {}
                cache[guild]['status'] = 'disabled'

                db.execute(f"SELECT _channel FROM starboard WHERE guild = 'guild'")
                channel = db.fetchone()

                cache[guild]['channel'] = channel[0]
            else:
                cache[guild]['status'] = 'disabled'

            with open('starboard.json', 'w') as g:
                json.dump(cache, g)

        except:
            await ctx.send("Starboard was never enabled for this server")

    @starboard_commands.command(name='enable', help="Enable starboard")
    async def enable_starboard(self, ctx):
        guild = str(ctx.guild.id)
        with open('starboard.json', 'r') as f:
            cache = json.load(f)

        try:
            db.execute(f"UPDATE Starboard SET _status = 'enabled' WHERE guild = '{ctx.guild}'")
            conn.commit()
            await ctx.send("Enabled starboard for this server")

            if guild not in cache:
                cache[guild] = {}
                cache[guild]['status'] = 'enabled'
                db.execute(f"SELECT _channel FROM starboard WHERE guild = 'guild'")
                channel = db.fetchone()
                cache[guild]['channel'] = channel[0]
            else:
                cache[guild]['status'] = 'enabled'

            with open('starboard.json', 'w') as g:
                json.dump(cache, g)

        except:
            await ctx.send("Starboard has not been set in this server. First run the `starboard channel` command")


def setup(client):
    client.add_cog(StarboardCommands(client))