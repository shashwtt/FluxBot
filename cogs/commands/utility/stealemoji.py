import discord
import requests
import shutil
import hex_colors

from discord.ext import commands


class StealEmoji(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name="stealemoji",
        aliases=["steal-emoji", "emojiadd", "se"],
        description="Download emojis that you have access to and upload them to your own server."
    )
    @commands.has_permissions(manage_emojis=True)
    async def steal(self, ctx, emoji_name, custom_emoji_name=None):
        image = None

        if len(ctx.message.attachments) == 0:
            image = emoji_name
            emoji_name = None
            image_url = None

        if len(ctx.message.attachments) > 0:
            image_url = ctx.message.attachments[0].url
            custom_emoji_name = emoji_name

        if image:
            try:
                try:
                    image = await discord.ext.commands.PartialEmojiConverter.convert(self, ctx=ctx, argument=image)
                except commands.BadArgument or commands.CommandError as e:
                    await ctx.send("An error occured while stealing the emoji from that source. Sorry")
                    return

                if custom_emoji_name:
                    emoji_name = custom_emoji_name
                else:
                    custom_emoji_name = image.name

                image_url = image.url

            except commands.BadArgument:
                image_url = image

        try:
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                with open(f"./emojis/{custom_emoji_name}.gif", "wb") as img:
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, img)

            else:
                raise Exception(f"Bad status code uploading {custom_emoji_name} received: {response.status_code}")

            with open(f"./emojis/{custom_emoji_name}.gif", "rb") as image:
                try:
                    if isinstance(ctx, discord.Guild):
                        new_emoji = await ctx.create_custom_emoji(name=custom_emoji_name, image=image.read())
                    else:
                        new_emoji = await ctx.message.guild.create_custom_emoji(name=custom_emoji_name, image=image.read())

                    embed = discord.Embed(
                        title="Emoji added successfully",
                        colour=hex_colors.l_green,
                        description=f"`:{custom_emoji_name}:`"
                    )
                    embed.set_thumbnail(url=image_url)

                    await ctx.message.channel.send(embed=embed)

                except discord.errors.HTTPException as e:
                    if e.code == 400:
                        await ctx.send("Only letters, numbers and underscores are allowed in emoji names.")
                        return

                except Exception as e:
                    print(e)

        except requests.exceptions.MissingSchema:
            await ctx.send(f"`{image_url}` doesn't seem like an emoji or an image")


def setup(client):
    client.add_cog(StealEmoji(client))