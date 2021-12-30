import asyncio
import random

import discord
import requests

import hex_colors

from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, Cog


class RPS(Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="rps", help="Play rock, paper, scissors with me :)", aliases=["rockpaperscissors"])
    async def rock_paper_scissors(self, ctx):
        choices = {
            0: "rock",
            1: "paper",
            2: "scissors"
        }
        reactions = {
            "🪨": 0,
            "🧻": 1,
            "✂": 2
        }
        embed = discord.Embed(title="Please choose", color=0xF59E42)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        choose_message = await ctx.send(embed=embed)
        for emoji in reactions:
            await choose_message.add_reaction(emoji)

        def check(reaction, user):
            return user == ctx.message.author and str(reaction) in reactions

        try:
            reaction, user = await self.client.wait_for("reaction_add", timeout=10, check=check)

            user_choice_emote = reaction.emoji
            user_choice_index = reactions[user_choice_emote]

            bot_choice_emote = random.choice(list(reactions.keys()))
            bot_choice_index = reactions[bot_choice_emote]

            result_embed = discord.Embed(color=0x42F56C)
            result_embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
            await choose_message.clear_reactions()

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
                await choose_message.add_reaction("🇱")
            await choose_message.edit(embed=result_embed)
        except asyncio.exceptions.TimeoutError:
            await choose_message.clear_reactions()
            timeout_embed = discord.Embed(title="Too late", color=0xE02B2B)
            timeout_embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
            await choose_message.edit(embed=timeout_embed)


def setup(client):
    client.add_cog(RPS(client))
