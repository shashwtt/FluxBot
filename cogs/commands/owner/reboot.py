import os

import discord
import heroku3
import hex_colors
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()


class Reboot(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.is_owner()
    @commands.command(
        name="reboot",
        aliases=['restart'],
        help="Stops the bot and starts it again...",
    )
    async def shutdown(self, ctx):
        async def view_timeout():
            timeup_embed = discord.Embed(
                description="Welp! fine not doing that"
            )
            await choices.edit(embed=timeup_embed, view=None)
            await choices.delete(delay=5)
            return

        async def cancel_click(interaction):
            if interaction.user.guild_permissions.administrator:
                await interaction.message.edit(embed=discord.Embed(description=f"Cancelled bot restart!", colour=hex_colors.l_green), view=None)
                await choices.delete(delay=5)
                view.stop()
                return
            else:
                pass

        async def ok_click(interaction):
            if interaction.user == ctx.author:
                embed = discord.Embed(
                    description="Restarting the bot! This may take a few seconds....",
                    color=0x42F56C
                )
                await ctx.send(embed=embed)
                heroku_ = heroku3.from_key(os.getenv("heroku_key"))
                flux_app = heroku_.apps()['flux-discord']
                flux_app.restart()
            else:
                pass

        view = discord.ui.View(timeout=15)
        ok_butt = discord.ui.Button(label="Restart!", style=discord.ButtonStyle.green)
        ok_butt.callback = ok_click
        view.add_item(ok_butt)
        cancel_butt = discord.ui.Button(label="Cancel!", style=discord.ButtonStyle.danger)
        cancel_butt.callback = cancel_click
        view.add_item(cancel_butt)
        view.on_timeout = view_timeout

        confirmation = discord.Embed(
            description=f"Are you sure you want to restart the bot?",
            color=0xF59E42
        )
        choices = await ctx.send(embed=confirmation, view=view)


def setup(client):
    client.add_cog(Reboot(client))
