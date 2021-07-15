import os
import time


import dotenv
import discord
from discord.ext import commands, tasks
from app.utils.logging import log


class Bot(commands.Bot):

    def __init__(self, prefix):
        super(Bot, self).__init__(
            command_prefix=prefix,
            intents=discord.Intents.all()
        )

        self.remove_command('help')
        log('Loading bot extensions')

        for filename in os.listdir("app/cogs"):  # Loads every extensions.
            if not filename.endswith(".py"):
                continue

            self.load_extension(f"app.cogs.{filename[:-3]}")
            log('-', filename)

        log(len(self.cogs), 'extensions loaded')

    def run(self):
        super().run(dotenv.dotenv_values('.env').get('TOKEN'))

    async def on_connect(self):
        log(f"Logged in as {self.user} after {time.perf_counter():,.3f}s")
        self.set_activity.start()

    async def on_ready(self):
        log(f"{self.user} Ready after {time.perf_counter():,.3f}s")

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