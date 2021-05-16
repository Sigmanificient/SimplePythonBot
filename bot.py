import os
import platform
import time
from datetime import datetime

import discord
from discord.ext import commands, tasks

LOG_FORMAT = '%d/%b/%Y:%H:%M:%S'


class Bot(commands.Bot):

    def __init__(self, prefix):
        super(Bot, self).__init__(
            command_prefix=f'{"local" * self.is_local}{prefix}',
            intents=discord.Intents.all()
        )

        self.remove_command('help')
        self.log('Loading bot extensions')

        for filename in os.listdir("cogs"):  # Loads every extensions.
            if not filename.endswith(".py"):
                continue

            self.load_extension(f"cogs.{filename[:-3]}")
            self.log('-', filename)

        self.log(len(self.cogs), 'extensions loaded')

    async def on_connect(self):
        self.log(f"Logged in as {self.user} after {time.perf_counter():,.3f}s")
        self.set_activity.start()

    async def on_ready(self):
        self.log(f"Ready after {time.perf_counter():,.3f}s")

    @tasks.loop(seconds=10)
    async def set_activity(self):
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{self.command_prefix}help ◈ ping: {self.latency * 1e3:.2f} ms"
            )
        )

    def embed(self, **kwargs):
        _embed = discord.Embed(**kwargs)

        return _embed.set_footer(
            text=f'{self.user.name} - {self.command_prefix}help for more information',
            icon_url=self.user.avatar_url
        )

    @staticmethod
    def log(*args):
        print(f"[{datetime.now().strftime(LOG_FORMAT)}]", *args)

    @property
    def is_local(self):
        return platform.system() == "Windows"

    @property
    def token(self):
        if not self.is_closed:
            return

        with open('storage/_token') as f:
            return f.read()


client = Bot('-')
client.run(client.token)  # Starts the bot
