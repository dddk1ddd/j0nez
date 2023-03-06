import discord
import openai
import os
from do_messages import do_messages
from loghandling import do_log
from formatting import cmdtxt, debugtxt, reset
from discord.ext import commands
from dotenv import load_dotenv
import tracemalloc

# debug
tracemalloc.start()

# j0nez ChatGPT bot v.011z by PK
# www.phatkid.art

intents = discord.Intents.default()
intents.message_content = True

load_dotenv()

# Authentication
token = os.getenv('TOKEN')
# openai.api_key = 'x'
openai.api_key = str(os.getenv('KEY'))

# Bot responds to "!" prefix.
# Todo: does not show up in server commands.
client = commands.Bot(
    command_prefix='!',
    self_bot=False,
    intents=intents
)

cog_files = ['image_cmnds', 'rolesystem', 'basic']


async def load_cogs():
    global client
    global cog_files
    for cog_file in cog_files:
        await client.load_extension(cog_file)
        print(cmdtxt + "Loading %s ..." % cog_file + reset)


class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=discord.Color.blurple(), description='')
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)


client.help_command = MyHelpCommand()


@client.event
async def on_message(message):
    # Ignore own self
    if message.author == client.user:
        await do_log(message, "self ")
        return
    await do_messages(client, message)


@client.event
async def on_message_edit(before, after):
    await do_log(before, "edit-")
    await do_log(after, "edit+")
    await do_messages(client, after)


@client.event
async def on_command_error(ctx, error):
    await do_log(ctx.message, "error")
    channel = ctx.message.channel
    if isinstance(error, commands.MissingRequiredArgument):
        await channel.send("Missing required argument: {}".format(error.param))
    elif isinstance(error, commands.BadArgument):
        await channel.send("Bad argument.")


@client.event
async def on_ready():
    await load_cogs()
    print(debugtxt + 'Logged in as' + reset)
    print(cmdtxt + str(client.user.name) + reset)
    print(cmdtxt + str(client.user.id) + reset)
    print(debugtxt + '------' + reset)


client.run(token, log_handler=None)
