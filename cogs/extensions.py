from time import time

from discord import Color
from discord.ext import commands


STATUS: tuple = ("🟥 disabled", "🟩 active")


class Extensions(commands.Cog):
    """ One extension to rule them all """
    hidden: bool = True

    def __init__(self, client):
        self.client = client

    async def modify_cog(self, ctx, cog):
        _started: float = time()
        _type: str = ctx.command.name
        cog_name: str = cog.capitalize()
        cog: str = f'cogs.{cog.lower()}'
        _embed = None

        try:
            if _type != 'load':
                self.client.unload_extension(cog)

            if _type != 'unload':
                self.client.load_extension(cog)

            time_elapsed = (time() - _started) * 1000

            _embed = self.client.embed(
                title=f'Successfully {ctx.command.name}ed',
                description=f'Successfully {ctx.command.name}ed `{cog_name}` under `{time_elapsed:.3}` ms',
                color=Color.green(),
            )

        except Exception as e:
            _embed = self.client.embed(
                title="Error !",
                description=f"An error occurred while {ctx.command.name}ing the extension {cog_name}",
                color=Color.red()
            )

            _embed.add_field(name='Error :', value=f'>>> ```\n{str(e)}```')

        finally:
            await ctx.send(embed=_embed)


def setup(client):
    client.add_cog(Extensions(client))
