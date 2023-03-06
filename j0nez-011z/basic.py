from discord.ext import commands
import time


class Basic(commands.Cog):
    @commands.command(
        name="version",
        help="j0nez v.011z by PK - http://www.phatkid.art"
    )
    async def version(self, ctx):
        await ctx.send("j0nez v.011z by PK - http://www.phatkid.art")

    @commands.command(
        name="ping",
        help="keepalive"
    )
    async def ping(self, ctx):
        await ctx.send("Pong! Somewhere right now it is " + str(time.asctime()))


async def setup(client):
    await client.add_cog(Basic(client))
