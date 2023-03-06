from discord.ext import commands


class RoleSystem(commands.Cog):
    @commands.command()
    async def listroles(self, ctx):
        roles = ctx.guild.roles
        role_names = [role.name for role in roles]
        role_names.remove('@everyone')  # remove the default role '@everyone' from the list
        role_list = '\n'.join(role_names)
        await ctx.send(f"Roles in this server:\n{role_list}")


async def setup(client):
    await client.add_cog(RoleSystem(client))
