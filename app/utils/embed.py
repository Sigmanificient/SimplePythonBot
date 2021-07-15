import discord


class Embed(discord.Embed):

    @classmethod
    def load(cls, client):
        cls.client = client
        return cls

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_footer(
            text=f'{self.client.user.name} - {self.client.command_prefix}help for more information',
            icon_url=self.client.user.avatar_url
        )
