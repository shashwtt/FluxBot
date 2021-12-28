import discord

from discord.ext import commands
from pytz import timezone
from datetime import datetime
from asyncio import sleep


class onReady(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.member_count = self.get_member_count()

    def get_member_count(self):
        karen = self.client.users
        return len(karen)

    async def status(self):
        while True:
            await self.client.wait_until_ready()
            await self.client.change_presence(
                activity=discord.Activity(type=discord.ActivityType.listening,
                                          name=f'.help')
            )  # listening to -help
            await sleep(10)
            await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                        name=f" {len(self.client.guilds)} servers")
                                              )  # watching x servers
            await sleep(10)
            await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                        name=f" {self.get_member_count()} users")
                                              )  # watching x users
            await sleep(10)

    @commands.Cog.listener()
    async def on_ready(self):
        print('--------------')
        print('All cogs loaded')
        # Since I host the bot on heroku, I'd like to know in the logs when the bot started/restarted in my own timezone
        print("Date:", datetime.now(timezone('Asia/Kolkata')).strftime('%d - %m - %Y'))
        print("Time:", datetime.now(timezone('Asia/Kolkata')).strftime('%H:%M'))
        print(f"Servers: {(len(self.client.guilds))}")
        print(f"Users: {self.member_count}")
        print("-------------------")
        self.client.loop.create_task(self.status())


def setup(client):
    client.add_cog(onReady(client))