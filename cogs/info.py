from time import perf_counter
from discord.ext import commands


class Utils(commands.Cog):
    """ A template cog """
    hidden: bool = False

    def __init__(self, client):
        self.client = client

    @commands.command(
        name='help',
        aliases=('all', 'all_cmds', 'cmds'),
        brief="List every command osf the bot"
    )
    @commands.cooldown(2, 60, commands.BucketType.user)
    async def all_commands(self, ctx):
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
    @commands.cooldown(2, 60, commands.BucketType.user)
    async def ping(self, ctx):
        """ Get the latency of the client converted in milliseconds.
        An dynamically colored ball will show in the image in function of the ping.
        Give also worst, best and daily average ping """
        latencies: dict = {"API": self.client.latency}

        marker: float = perf_counter()
        ping_message = await ctx.send('> pinging...')
        latencies["BOT"] = perf_counter() - marker

        _embed = self.client.embed(
            title=f'{ctx.author.name} Ponged !',
            description="The bot, bd & API latency"
        )

        for k, v in latencies.items():
            _embed.add_field(name=f"{k} latency", value=f'> `{v * 1e3:,.2f} ms`')

        await ping_message.edit(content=' ', embed=_embed)


def setup(client):
    client.add_cog(Utils(client))
