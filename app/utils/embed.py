from __future__ import annotations
from typing import Type, Tuple, TYPE_CHECKING

import discord

if TYPE_CHECKING:
    from app.bot import Bot


class Embed(discord.Embed):

    @classmethod
    def load(cls, client: Bot) -> Type[Embed]:
        cls.client: Bot = client
        return cls

    def __init__(self, **kwargs: Tuple[str]) -> None:
        super().__init__(**kwargs)

        self.set_footer(
            text=f'{self.client.user.name} - {self.client.command_prefix}help for more information',
            icon_url=self.client.user.avatar_url
        )
