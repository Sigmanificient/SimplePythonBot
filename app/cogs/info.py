from time import perf_counter
from platform import python_version

import discord
from discord.ext import commands


class Info(commands.Cog):
    """Group of commands related to information on the bot."""

    def __init__(self, client):
        self.client = client

    @commands.command(
        name='help',
        aliases=('all', 'all_cmds', 'cmds'),
        brief="List every command osf the bot"
    )
    async def help_command(self, ctx):
        """ Provide a list of every command available command for the user,
        split by extensions and organized in alphabetical order.
        Will not show the event-only extensions """

        _embed = self.client.embed(
            title='All commands',
            description=f"> `{len(self.client.commands)}` commands available"
        )

        for cog_name, cog in self.client.cogs.items():
            if len(cog.get_commands()):
                _embed.add_field(
                    name=cog_name.capitalize(),
                    value='  •  '.join(sorted(f'`{c.name}`' for c in cog.get_commands())),
                    inline=False
                )

        await ctx.send(embed=_embed)

    @commands.command(
        name='ping',
        aliases=('latency', 'lat', 'ms'),
        brief='Pong !'
    )
    async def ping_command(self, ctx):
        """ Get the latency of the client converted in milliseconds.
        An dynamically colored ball will show in the image in function of the ping.
        Give also worst, best and daily average ping """
        ping_embed = self.client.embed(
            title=f'{ctx.author.name} Ponged !',
            description="The bot, bd & API latency"
        )

        ping_embed.add_field(name="API latency", value=f"> `{self.client.latency * 1e3:,.2f}` ms")

        marker: float = perf_counter()
        await ctx.send(embed=ping_embed)

        elapsed = perf_counter() - marker
        ping_embed.add_field(name="Bot latency", value=f"> `{elapsed * 1e3:,.2f}` ms")
        await ping_embed.edit(embed=ping_embed)

    @commands.command(
        name='bot',
        brief="Display the bot information"
    )
    async def client_information_command(self, ctx):
        """ Display the bot information """
        info_embed = self.client.embed(
            title=f'{self.client.user_command.name} Bot Information',
            description='\n'.join(
                (
                    'This bot have been created, coded and is owned by Sigmanificient#3301',
                    self.client.user_command.created_at.strftime("> **Creation date** : %A %d %B %Y at %H:%M")
                )
            )
        )

        for key, val in {
            'Python': python_version(),
            'Discord': discord.__version__,
            'Commands': len(self.client.commands),
            'Extensions': len(self.client.cogs)
        }.items():
            info_embed.add_field(name=key, value=f'> `{val}`', inline=True)

        await ctx.send(embed=info_embed)

    @commands.command(
        name="invite",
        aliases=("inv", "i"),
        brief="A link to invite the bot"
    )
    async def invite(self, ctx):
        await ctx.send(
            embed=self.client.embed(
                title="Invite the Bot !",
                description='\n'.join(
                    (
                        "> Click this link to invite this bot on your servers !",
                        "You need to have permissions on the server to use the link",
                        "[invite me now](https://discord.com/api/oauth2/authorize?client_"
                        f"id={self.client.user_command.id}&permissions=8&scope=bot)"
                    )
                )
            )
        )


def setup(client):
    client.add_cog(Info(client))
