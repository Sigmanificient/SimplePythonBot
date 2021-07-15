from os import listdir
from time import perf_counter
from typing import Optional

from discord import Color
from discord.ext import commands

from app.bot import Bot
from app.utils.embed import Embed

STATUS: tuple = ("🟥 disabled", "🟩 active")


class Extensions(commands.Cog):
    """One extension to rule them all."""

    def __init__(self, client: Bot):
        """Initialise the Extensions cog."""
        self.client: Bot = client

    async def alter_cogs(self, ctx: commands.Context, cog: str) -> None:
        marker: float = perf_counter()
        _type: str = ctx.command.name
        cog_name: str = cog.capitalize()
        cog: str = f'cogs.{cog.lower()}'

        result_embed: Optional[Embed] = None

        try:
            if _type != 'load':
                self.client.unload_extension(cog)

            if _type != 'unload':
                self.client.load_extension(cog)

        except Exception as e:
            result_embed: Embed = self.client.embed(
                title="Error !",
                description=f"An error occurred while {ctx.command.name}ing the extension {cog_name}",
                color=Color.red()
            )

            result_embed.add_field(name='Error :', value=f'>>> ```\n{str(e)}```')

        else:
            time_elapsed: float = (perf_counter() - marker) * 1000

            result_embed: Embed = self.client.embed(
                title=f'Successfully {ctx.command.name}ed',
                description=f'Successfully {ctx.command.name}ed `{cog_name}` under `{time_elapsed:.3}` ms',
                color=Color.green(),
            )

        finally:
            await ctx.send(embed=result_embed)

    @commands.command(
        name='load',
        brief="Load an extension on the bot"
    )
    @commands.is_owner()
    async def load_extension(self, ctx: commands.Context, cog: str) -> None:
        """ load the given extension ( cog ) given.

        The command can only be executed by the bot owner
        An not existing extension will return 'cannot be loaded' error """
        await self.alter_cogs(ctx, cog)

    @commands.command(
        name='unload',
        brief="Unload an active extension"
    )
    @commands.is_owner()
    async def unload_extension(self, ctx: commands.Context, cog: str) -> None:
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
    async def reload_extension(self, ctx: commands.Context, cog: str) -> None:
        """ Reload the given extension ( cog ).

        The command can only be executed by the bot owner
        An not existing extension will return 'not been loaded' error
        Reload an extension will apply newest change to the code """
        await self.alter_cogs(ctx, cog)

    @commands.command(
        name="extensions",
        aliases=['ext'],
        brief="List all extensions"
    )
    @commands.is_owner()
    async def list_cogs(self, ctx: commands.Context) -> None:
        """Returns a list of all enabled and disabled extensions."""

        cogs_list_embed: Embed = self.client.embed(
            title="All extensions",
            description='>>> %s' % '\n'.join(STATUS)
        )

        for filename in listdir('app/cogs'):
            if filename.endswith('.py'):
                cogs_list_embed.add_field(
                    name=filename,
                    value=STATUS[filename[:-3].capitalize() in self.client.cogs.keys()]
                )

        await ctx.send(embed=cogs_list_embed)

    @staticmethod
    async def on_command_error(ctx: commands.Context, error: Exception) -> None:
        """Handle is owner errors."""

        if isinstance(error, commands.NotOwner):
            await ctx.send("You do not own this bot.")


def setup(client: Bot) -> None:
    """Load the extension into the bot."""
    client.add_cog(Extensions(client))
