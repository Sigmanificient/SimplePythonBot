import platform

import discord
from discord.ext import commands, tasks


class Bot(commands.Bot):

    def __init__(self, prefix):
        super(Bot, self).__init__(
            command_prefix=f'{"local" * self.is_local}{prefix}',
            intents=discord.Intents.all()
        )

        self.remove_command('help')

    async def on_ready(self):
        print("Connected as Bot:", self.user)

    @property
    def is_local(self):
        return platform.system() == "Windows"

    @property
    def token(self):
        f = open('storage/_token')
        try:
            if self.is_closed:
                return f.read()

        finally:
            f.close()


client = Bot('-')
client.run(client.token)  # Starts the bot
