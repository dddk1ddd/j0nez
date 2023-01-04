import discord
import openai
import requests
import os
import time
from discord.ext import commands
from dotenv import load_dotenv

# j0nez ChatGPT bot v.011c by PK
# www.phatkid.art

intents = discord.Intents.default()
intents.message_content = True

load_dotenv()

token = os.getenv('TOKEN')
apikey = str("Bearer " + str(os.getenv('KEY')))
openai.api_key = str(os.getenv('KEY'))
client = commands.Bot(
    command_prefix='!',
    self_bot=False,
    intents=intents
)


class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=discord.Color.blurple(), description='')
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)


client.help_command = MyHelpCommand()


@client.command(
    name="version",
    help="j0nez v.011c by PK - www.phatkid.art"
)
async def version(ctx):
    await ctx.send("j0nez v.011c by PK - www.phatkid.art")


@client.command(
    name="ping",
    help="keepalive"
)
async def ping(ctx):
    await ctx.send("Pong! Somewhere right now it is " + str(time.asctime()))


@client.command(
    name="image",
    help="""
    AI generated image from a description.
    The more descriptive, the better.
    """
)
async def image(ctx, *, description):
    prompt = ' '.join(description)
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        output = response['data'][0]['url']
        await ctx.send(output)
    except openai.error.OpenAIError as e:
        await ctx.send("Error Code: " + str(e.http_status))
        await ctx.send(e.error)


@client.command(
    name="remix",
    help="""
    !remix <prompt> <image> <mask>
    prompt
    A text description of the desired image.
    image
    The image to edit. Must be a valid PNG file,
    less than 4MB, and square. Works best with !image.
    mask
    An additional image whose fully transparent areas indicate
    where image should be edited. Must be a valid PNG file,
    less than 4MB, and have the same dimensions as image.
    """
)
async def remix(ctx):
    prompt = ctx.message.content
    try:
        image = ctx.message.attachments[0]
        image_data = await image.read()
        mask = ctx.message.attachments[1]
        mask_data = await mask.read()
    except:
        await ctx.send("You must provide two square PNG files less than 4MB each.")
    try:
        response = openai.Image.create_edit(
            image_data,
            mask_data,
            prompt=prompt,
            n=1,
            size="512x512"
        )
        output = response['data'][0]['url']
        await ctx.send(output)
    except openai.error.OpenAIError as e:
        await ctx.send("Error Code: " + str(e.http_status))
        await ctx.send(e.error)



@client.command(
    name="morph",
    help="""
    Morphs an image [number] of times,
    with a maximum of 10.
    Must be a square PNG less than 4MB.
    Works best with images from !image.
    """
)
async def morph(ctx, number=1):
    image = ctx.message.attachments[0]
    image_data = await image.read()
    try:
        response = openai.Image.create_variation(
            image_data,
            n=number,
            size="512x512"
        )
        for i in range(int(number)):
            output = response['data'][i]['url']
            await ctx.send(output)
    except openai.error.OpenAIError as e:
        await ctx.send("Error Code: " + str(e.http_status))
        await ctx.send(e.error)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    # Ignore own self
    if message.author == client.user:
        return
    # Process bot commands
    await client.process_commands(message)
    if message.content.startswith("!"):
        return
    # I was mentioned
    if client.user in message.mentions:
        # Send a message in response to the mention
        prompt = message.content
        url = "https://api.openai.com/v1/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": apikey,
        }
        data = {
            "model": "text-davinci-003",
            "prompt": prompt,
            "max_tokens": 4000,
            "temperature": 1,
            "presence_penalty": -2,
            "frequency_penalty": 2
        }
        response = requests.post(url, headers=headers, json=data)
        output = response.json()['choices'][0]['text']
        await message.channel.send(output)
        return

client.run(token)
