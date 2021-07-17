import os
import time
from datetime import datetime
from typing import Union, Any, Tuple

import dotenv
import discord
from discord.ext import commands, tasks


class Bot(commands.Bot):

    def __init__(self, prefix) -> None:
        """Initializing bot and load extensions."""
        super(Bot, self).__init__(
            command_prefix=prefix,
            intents=discord.Intents.all()
        )

        self.remove_command('help')
        self.load_extensions()

    def load_extensions(self) -> None:
        """Loading every extensions in cogs folder."""
        self.log('Loading bot extensions')

        for filename in os.listdir("cogs"):
            if not filename.endswith(".py"):
                continue

            self.log('-', filename)
            name: str = filename[:-3]

            try:
                super().load_extension(f"cogs.{name}")

            except commands.ExtensionFailed as error:
                print("[Warning]", f"Could not load component '{name}' due to {error.__cause__}")

            else:
                self.log(len(self.cogs), 'extensions loaded')

    async def on_connect(self) -> None:
        """Event called when bot Successfully connects to discord account."""
        self.log(f"Logged in as {self.user} after {time.perf_counter():,.3f}s")
        self.set_activity.start()

    async def on_ready(self) -> None:
        """Event called when bot is ready to be used."""
        self.log(f"{self.user} Ready after {time.perf_counter():,.3f}s")

    @tasks.loop(seconds=10)
    async def set_activity(self) -> None:
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{self.command_prefix}help ◈ ping: {self.latency * 1e3:.2f} ms"
            )
        )

    def log(*args: Union[Any, Tuple[Any]]) -> None:
        """Prints a formatted log message."""
        print(f"[{datetime.now():%d/%b/%Y:%H:%M:%S}]", *args)

    def embed(self, **kwargs):
        return discord.Embed(**kwargs).set_footer(
            text=f'{self.user.name} - {self.command_prefix}help for more information',
            icon_url=self.user.avatar_url
        )


def main() -> None:
    """Entry point to load the app."""
    client: Bot = Bot('&')
    client.run(dotenv.dotenv_values('.env').get('TOKEN'))


if __name__ == '__main__':
    main()
