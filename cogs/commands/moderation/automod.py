import discord
import hex_colors
import json

from discord.ext import commands
from db import *


class AutoModCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(name='automod', aliases=['am'], help="Configure AutoMod for the server",
                    invoke_without_command=True)
    @commands.has_permissions(manage_messages=True)
    async def automod_cmds(self, ctx):
        em = discord.Embed(
            title="Available commands:",
            description="""
`enable`
`disable`
`blacklist`
`remove`
`show`
""")
        em.set_footer(text="Use 'automod <command>' to use a command")

        if not ctx.guild.me.guild_permissions.manage_messages:
            await ctx.send("I need the `Manage Messages` permission for Auto moderation")
            return

        await ctx.send(embed=em)

    @automod_cmds.command(name='enable')
    async def automod_enable(self, ctx):
        try:
            db.execute(f"INSERT INTO AutoMod(guild, _status) VALUES('{ctx.guild.id}','enabled')")
            db.execute(f"CREATE TABLE IF NOT EXISTS am_{ctx.guild.id}(words VARCHAR(40) PRIMARY KEY)")
            conn.commit()
        except:
            db.execute(f"UPDATE AutoMod SET _status = 'enabled' WHERE guild = '{ctx.guild.id}'")
            conn.commit()
        finally:
            # Add in cache
            with open('automod.json', 'r') as f:
                cache = json.load(f)

            if str(ctx.guild.id) not in cache:
                cache[str(ctx.guild.id)] = {}
                cache[str(ctx.guild.id)]['status'] = 'enabled'
                cache[str(ctx.guild.id)]['blacklist'] = []

                with open('automod.json', 'w') as f:
                    json.dump(cache, f)

            await ctx.send("Enabled Auto Mod for your server")

    @automod_cmds.command(name='disable')
    async def automod_disable(self, ctx):
        db.execute(f"UPDATE AutoMod SET _status = 'disabled' WHERE guild = '{ctx.guild.id}'")
        conn.commit()
        await ctx.send("Disabled Auto Mod for your server")

        with open('automod.json', 'r') as f:
            cache = json.load(f)

        cache[str(ctx.guild.id)] = {}
        cache[str(ctx.guild.id)]['status'] = 'disabled'
        cache[str(ctx.guild.id)]['blacklist'] = []

        with open('automod.json', 'w') as f:
            json.dump(cache, f)

    async def get_status(self, guild):
        with open('automod.json', 'r') as f:
            cache = json.load(f)

        if guild not in cache:
            db.execute(f"SELECT _status FROM AutoMod WHERE guild = '{guild}'")
            status = db.fetchone()

            cache[guild] = {}
            cache[guild]['blacklist'] = []
            cache[guild]['status'] = status[0]
            with open('automod.json', 'w') as f:
                json.dump(cache, f)
        else:
            status = cache[str(guild)]['status']
        return status

    @automod_cmds.command(name='blacklist', aliases=['bl', 'ban'])
    async def automod_blacklist(self, ctx, *, word):
        if len(word) > 40:
            await ctx.send("Word length cannot exceed 40 characters")
            return

        db.execute(f"CREATE TABLE IF NOT EXISTS am_{ctx.guild.id}(words VARCHAR(40) PRIMARY KEY)")
        db.execute(f"INSERT INTO am_{ctx.guild.id} (words) VALUES ('{word}')")
        conn.commit()
        await ctx.send(f"||{word}|| is now blacklisted from the server")

        status = await self.get_status(ctx.guild.id)
        if status == 'disabled' or status is None:
            await self.automod_enable(ctx)

        # Cache
        with open('automod.json', 'r') as f:
            cache = json.load(f)

        if str(ctx.guild.id) not in cache:
            cache[str(ctx.guild.id)] = {}
            cache[str(ctx.guild.id)]['status'] = 'enabled'
            cache[str(ctx.guild.id)]['blacklist'] = []
        else:
            cache[str(ctx.guild.id)]['blacklist'].append(str(word))

        with open('automod.json', 'w') as f:
            json.dump(cache, f)

    @automod_cmds.command(name='remove', aliases=['rm', 'unban'])
    async def automod_remove(self, ctx, *, word):
        guild = str(ctx.guild.id)
        status = await self.get_status(ctx.guild.id)
        if status == 'disabled' or status is None:
            await self.automod_enable(ctx)
        with open('automod.json', 'r') as f:
            cache = json.load(f)

        if guild not in cache:
            db.execute(f"SELECT * FROM am_{ctx.guild.id}")
            lst = db.fetchall()
            blacklist = []
            for _word in lst:
                blacklist.append(_word[0])

            cache[guild] = {}
            cache[guild]['blacklist'] = blacklist

            if word not in blacklist:
                await ctx.send("That word isn't blacklisted")

        db.execute(f"DELETE FROM am_{ctx.guild.id} WHERE words = '{word}'")
        conn.commit()
        try:
            cache[guild]['blacklist'].remove(word)
        except ValueError:
            pass

        with open('automod.json', 'w') as f:
            json.dump(cache, f)

        await ctx.send(f'Un-blacklisted `{word}`')

    @automod_cmds.command(name='show', aliases=['list'])
    async def automod_show(self, ctx):
        guild = str(ctx.guild.id)
        status = await self.get_status(ctx.guild.id)

        if status == 'disabled' or status is None:
            await self.automod_enable(ctx)

        with open('automod.json', 'r') as f:
            cache = json.load(f)

        desc = ''

        if guild not in cache:
            db.execute(f"SELECT * FROM am_{ctx.guild.id}")
            lst = db.fetchall()

            for word in lst:
                desc += f"`{word[0]}`\n"  # word is a tuple
                cache['blacklist'].append(word[0])
            if desc is None:
                desc = f"{ctx.guild.name} has no blacklisted words"

            with open('automod.json', 'w') as f:
                json.dump(cache, f)
        else:
            for word in cache[guild]['blacklist']:
                desc += f"`{word}`\n"

        if desc == '':
            desc = 'No words blacklisted in your server'

        em = discord.Embed(
            title=f'Blacklisted words in {ctx.guild.name}',
            description=desc,
            color=hex_colors.m_red
        )
        await ctx.send(embed=em)


def setup(client):
    client.add_cog(AutoModCommands(client))