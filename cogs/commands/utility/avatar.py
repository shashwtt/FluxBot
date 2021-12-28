import discord
import random
import hex_colors

from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, Cog

class Avatar(Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='avatar', aliases=['av'], help="Show a user's avatar in full size")
    @cooldown(1, 5,  BucketType.user)
    async def avatar(self, ctx, user:discord.Member=None):
        member = user
        if member == None: #If no argument is passed
            member = ctx.author

        try:
            download_link = f"Download as [png]({member.avatar_url_as(format='png')}) | [jpeg]({member.avatar_url_as(format='jpeg')}) | [gif]({member.avatar_url_as(format='gif')})"
        except: #If the user's avatar wasn't animated
            download_link = f"Download as [png]({member.avatar_url_as(format='png')}) | [jpeg]({member.avatar_url_as(format='jpeg')}) | [webp]({member.avatar_url_as(format='webp')})"

        em = discord.Embed(title=f"{member.display_name}'s avatar", description=download_link, color=random.choice(hex_colors.colors))
        em.set_image(url=member.avatar_url)
        em.set_footer(text=f'Requested by {ctx.author.display_name}', icon_url=ctx.author.avatar_url)

        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Avatar(client))