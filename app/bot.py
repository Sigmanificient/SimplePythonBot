import os
import time

import dotenv
import discord
from discord.ext import commands, tasks
from app.utils.embed import Embed
from app.utils.logging import log, warn


class Bot(commands.Bot):

    def __init__(self, prefix) -> None:
        """Initializing bot and load extensions."""
        super(Bot, self).__init__(
            command_prefix=prefix,
            intents=discord.Intents.all()
        )

        self.embed = Embed.load(self)
        self.remove_command('help')
        self.load_extensions()

    def load_extensions(self) -> None:
        """Loading every extensions in cogs folder."""
        log('Loading bot extensions')

        for filename in os.listdir("app/cogs"):
            if not filename.endswith(".py"):
                continue

            self.load_extension(filename[:-3])
            log('-', filename)

        log(len(self.cogs), 'extensions loaded')

    def load_extension(self, name, *_) -> None:
        """Loads a given extension with a safe guard."""
        try:
            super().load_extension(f"app.cogs.{name}")

        except commands.ExtensionFailed as error:
            warn(f"Could not load component '{name}' due to {error.__cause__}")

    def unload_extension(self, name, *_) -> None:
        """Unloads a given extension."""
        super().unload_extension(f"app.cogs.{name}")

    def run(self) -> None:
        """Starting client with the token given in dotenv."""
        super().run(dotenv.dotenv_values('.env').get('TOKEN'))

    async def on_connect(self) -> None:
        """Event called when bot connects to the discord account."""
        log(f"Logged in as {self.user} after {time.perf_counter():,.3f}s")
        self.set_activity.start()

    async def on_ready(self) -> None:
        """Event called when bot is ready to be used."""
        log(f"{self.user} Ready after {time.perf_counter():,.3f}s")

    @tasks.loop(seconds=10)
    async def set_activity(self) -> None:
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=(
                    f"{self.command_prefix}help"
                    f" ◈ ping: {self.latency * 1e3:.2f} ms"
                )
            )
        )
