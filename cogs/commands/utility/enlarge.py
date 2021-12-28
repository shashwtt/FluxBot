import discord
import requests
import random
import hex_colors
import random
import shutil

from discord.ext import commands
from discord.ext.commands import PartialEmojiConverter


class EnlargeEmoji(commands.Cog):
    """
    This is going to be almost same as the steal_emoji.py
    """

    def __init__(self, client):
        self.client = client

    @commands.command(name='enlarge', aliases=["enlargeemoji"],
                      description="Enlarge emojis, you can download them too.")
    async def enlarge(self, ctx, emoji):
        await self.emoji_from_url(ctx, emoji)

    async def emoji_from_url(self, ctx, emoji, image=None):
        try:
            if image is None:
                image = emoji
                emoji = None

            image_url = None
            if image:
                try:
                    image = await discord.ext.commands.PartialEmojiConverter.convert(self, ctx=ctx, argument=image)
                    image_url = image.url

                except commands.BadArgument:
                    image_url = image


            await self.install_emoji(ctx, {"title": emoji, "image": image_url})
        except Exception:
            await ctx.send(embed=discord.Embed(
                title="No dumb!",
                description="Give me a Custom emoji not this"
            ))

    async def install_emoji(self, ctx, emoji_json):
        response = requests.get(emoji_json["image"], stream=True)
        if response.status_code == 200:  # If there were no errors
            with open(f"./emojis/{emoji_json['title']}.gif", "wb") as img:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, img)

        else:
            raise Exception(f"Bad status code uploading {emoji_json['title']} received: {response.status_code}")

        with open(f"./emojis/{emoji_json['title']}.gif", "rb") as image:
            embed = discord.Embed(colour=random.choice(hex_colors.colors))
            embed.set_image(url=emoji_json["image"])
            embed.set_footer(
                text="If the image is still small, maybe that's the original resolution. I can't do anything.")

            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(EnlargeEmoji(client))