from time import time

from discord import Color
from discord.ext import commands


STATUS: tuple = ("🟥 disabled", "🟩 active")


class Extensions(commands.Cog):
    """ One extension to rule them all """
    hidden: bool = True

    def __init__(self, client):
        self.client = client

    async def alter_cogs(self, ctx, cog):
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

    @commands.command(
        name='load',
        brief="Load an extension on the bot"
    )
    @commands.is_owner()
    async def load_extension(self, ctx, cog):
        """ load the given extension ( cog ) given.
        The command can only be executed by the bot owner
        An not existing extension will return 'cannot be loaded' error """
        await self.alter_cogs(ctx, cog)

    @commands.command(
        name='unload',
        brief="Unload an active extension"
    )
    @commands.is_owner()
    async def unload_extension(self, ctx, cog):
        """ Unload the given extension ( cog ).
        The command can only be executed by the bot owner
        An not existing extension will return 'not been loaded' error
        Unloading will remove all extension commands and data from the bot """
        await self.alter_cogs(ctx, cog)

    @commands.command(
        name='reload',
        brief="Reload an active extension"
    )
    @commands.is_owner()
    async def reload_extension(self, ctx, cog):
        """ Reload the given extension ( cog ).
        The command can only be executed by the bot owner
        An not existing extension will return 'not been loaded' error
        Reload an extension will apply newest change to the code """
        await self.alter_cogs(ctx, cog)


def setup(client):
    client.add_cog(Extensions(client))
