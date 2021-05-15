import discord
from discord.ext import commands, tasks


class Bot(commands.Bot):

    def __init__(self, **kwargs):
        super(Bot, self).__init__(**kwargs)

    @property
    def token(self):
        f = open('storage/_token')
        try:
            if self.is_closed:
                return f.read()

        finally:
            f.close()


client = Bot(command_prefix='-', intents=discord.Intents.all())
client.run(client.token)  # Starts the bot
