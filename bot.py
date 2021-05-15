import os
import platform
import time
from datetime import datetime

import discord
from discord.ext import commands

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

    async def on_ready(self):
        self.log(f"Logged in as {self.user} after {time.perf_counter():,.3f}s")

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
