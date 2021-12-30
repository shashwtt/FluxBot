import asyncio
import random
import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, Cog
from discord.ui import View, Button

class RPS(Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="rps", help="Play a calm game of rock, paper, scissors with me :)", aliases=["rockpaperscissors"])
    async def rock_paper_scissors(self, ctx):
        reactions = ["🪨", "🧻", "✂"]
        embed = discord.Embed(title=f"{ctx.author.display_name}, Please Choose an Option", color=0xF59E42)
        embed.set_footer(text='You have 10 seconds to choose!')

        view = View(timeout=10)

        async def view_timeout():
            timeout_embed = discord.Embed(title="Too late", color=0xE02B2B)
            timeout_embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
            await choose_message.edit(embed=timeout_embed, view=None)

        async def button_click0(interaction):
            await work(0)

        async def button_click1(interaction):
            await work(1)

        async def button_click2(interaction):
            await work(2)

        async def work(user_choice_index):
            bot_choice_index = random.randint(0, 2)
            bot_choice_emote = reactions[bot_choice_index]
            user_choice_emote = reactions[user_choice_index]

            print(bot_choice_index)
            print(user_choice_index)
            print(user_choice_emote)
            print(bot_choice_emote)

            result_embed = discord.Embed(color=0x42F56C)
            result_embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)

            if user_choice_index == bot_choice_index:
                result_embed.description = f"**That's a draw!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = 0xF59E42
            elif user_choice_index == 0 and bot_choice_index == 2:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = 0x42F56C
            elif user_choice_index == 1 and bot_choice_index == 0:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = 0x42F56C
            elif user_choice_index == 2 and bot_choice_index == 1:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = 0x42F56C
            else:
                result_embed.description = f"**I won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = 0xE02B2B

            await choose_message.edit(embed=result_embed, view=None)

        butt0 = Button(style=discord.ButtonStyle.blurple, emoji=f"{reactions[0]}")
        butt0.callback = button_click0

        butt1 = Button(style=discord.ButtonStyle.blurple, emoji=f"{reactions[1]}")
        butt1.callback = button_click1

        butt2 = Button(style=discord.ButtonStyle.blurple, emoji=f"{reactions[2]}")
        butt2.callback = button_click2

        view.add_item(butt0)
        view.add_item(butt1)
        view.add_item(butt2)

        choose_message = await ctx.send(embed=embed, view=view)

def setup(client):
    client.add_cog(RPS(client))
