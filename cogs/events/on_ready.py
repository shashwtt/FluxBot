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
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=".help"))


def setup(client):
    client.add_cog(onReady(client))