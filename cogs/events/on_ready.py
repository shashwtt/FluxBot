import discord

from discord.ext import commands
from pytz import timezone
from datetime import datetime
from asyncio import sleep


class onReady(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def status(self):
        while True:
            await self.client.wait_until_ready()
            await self.client.change_presence(
                activity=discord.Activity(type=discord.ActivityType.listening,
                                          name='-help')
            )  # listening to -help
            await sleep(5)
            await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                        name=f" {len(self.client.guilds)} servers")
                                              )  # watching x servers
            await sleep(5)
            await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                        name=f" {len(self.client.users)} users")
                                              )  # watching x users
            await sleep(5)

    @commands.Cog.listener()
    async def on_ready(self):
        print('--------------')
        print('All cogs loaded')
        # Since I host the bot on heroku, I'd like to know in the logs when the bot started/restarted in my own timezone
        print("Date:", datetime.now(timezone('Asia/Kolkata')).strftime('%d - %m - %Y'))
        print("Time:", datetime.now(timezone('Asia/Kolkata')).strftime('%H:%M'))
        print(f"Servers: {(len(self.client.guilds))}")
        print(f"Users: {len(self.client.users)}")
        print("-------------------")
        self.client.loop.create_task(self.status())


def setup(client):
    client.add_cog(onReady(client))
    print('onReady')
