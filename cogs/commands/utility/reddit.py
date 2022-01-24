import discord
import hex_colors
import random
import requests

from discord.ext import commands


class Reddit(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name='reddit',
        usage="<subreddit>",
        aliases=['subreddit', 'r'],
        help='Gets a post from the subreddit provided',
        description="Get a random post from the subreddit given and send it in the chat. This will also return nsfw posts, but is only sent if the channel is marked nsfw. If you don't want to see nsfw posts then run the command in a channel that is not nsfw!"
    )
    async def get_reddit_post(self, ctx, *, subreddit):
        if len(subreddit.split()) > 1:
            subreddit = subreddit.split()[0]

        url = f'https://meme-api.herokuapp.com/gimme/{subreddit}'  # This api only sends posts with images or gifs.

        post = requests.get(url=url).json()
        # Check if the post is nsfw
        if 'nsfw' in post:  # Sometimes it raises KeyError
            if post['nsfw']:
                if not ctx.channel.is_nsfw():
                    await ctx.reply("The post I got from that subreddit is marked NSFW. I cannot send it here", mention_author=False)
                    return

        try:
            image = post['url']  # the image
            title = post['title']  # the title of the reddit post
            link = post['postLink']  # the link to the post

            em = discord.Embed(
                title=title,
                description=link,
                color=random.choice(hex_colors.colors)
            )

            if len(em.title) > 256:
                em.title = "Title was too long for an embed."

            em.set_image(url=image)
            em.set_footer(
                text=f"👍 {post['ups']} | Author: u/{post['author']}")  # post['ups'] is the upvote count, post['author'] is the author

            await ctx.send(embed=em)

        except KeyError as e:
            if post["code"] == 400:
                if "no posts with images" in post["message"].lower():
                    await ctx.send("That subreddit doesn't have any posts with images")
                    return

            if post["code"] == 404:
                await ctx.send("This subreddit has no posts or doesn't exist.")
                return


def setup(client):
    client.add_cog(Reddit(client))