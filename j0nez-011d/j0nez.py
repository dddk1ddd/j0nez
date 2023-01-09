import discord
import openai
import os
import re
import time
from PIL import Image
from io import BytesIO
from colored import fg, bg, attr
from discord.ext import commands
from dotenv import load_dotenv

# j0nez ChatGPT bot v.011d by PK
# www.phatkid.art

intents = discord.Intents.default()
intents.message_content = True

load_dotenv()

# Authentication
token = os.getenv('TOKEN')
openai.api_key = str(os.getenv('KEY'))

client = commands.Bot(
    command_prefix='!',
    self_bot=False,
    intents=intents
)

# Console formatting
errtxt = bg('black') + fg('indian_red_1a')
cmdtxt = bg('black') + fg('dodger_blue_2')
debugtxt = bg('black') + fg('light_slate_blue')
chattxt = bg('black') + fg('white')
reset = attr('reset')


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
    help="j0nez v.011d by PK - http://www.phatkid.art"
)
async def version(ctx):
    print(cmdtxt + "#" + str(ctx.message.channel) + " - " +
          str(ctx.author) + "> " + str(ctx.message.content) + reset)
    await ctx.send("j0nez v.011d by PK - http://www.phatkid.art")


@client.command(
    name="ping",
    help="keepalive"
)
async def ping(ctx):
    print(cmdtxt + "#" + str(ctx.message.channel) + " - " +
          str(ctx.author) + "> " + str(ctx.message.content) + reset)
    await ctx.send("Pong! Somewhere right now it is " + str(time.asctime()))


@client.command(
    name="image",
    help="""
    Generate image from a description.
    """
)
async def image(ctx, *, description=''):
    prompt = ' '.join(description)
    print(cmdtxt + "#" + str(ctx.message.channel) + " - " +
          str(ctx.author) + "> " + str(ctx.message.content) + reset)
    try:
        await ctx.send("Working...")
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        output = response['data'][0]['url']
        await ctx.send(output)
        print(debugtxt + "Image Generated!" + reset)
    except openai.error.OpenAIError as e:
        errmsg = e.error['message']
        print(errtxt + "Error: " + errmsg + reset)
        await ctx.send(errmsg)


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
    print(cmdtxt + "#" + str(ctx.message.channel) + " - " +
          str(ctx.author) + "> " + str(ctx.message.content) + reset)
    try:
        image = ctx.message.attachments[0]
        image_data = await image.read()
        mask = ctx.message.attachments[1]
        mask_data = await mask.read()
    except:
        await ctx.send("Attach two square PNG files less than 4MB each.")
    try:
        await ctx.send("Remixing...")
        response = openai.Image.create_edit(
            image_data,
            mask_data,
            prompt=prompt,
            n=1,
            size="512x512"
        )
        output = response['data'][0]['url']
        await ctx.send(output)
        print(debugtxt + "Remixed!" + reset)
    except openai.error.OpenAIError as e:
        errmsg = e.error['message']
        print(errtxt + "Error: " + errmsg + reset)
        await ctx.send(errmsg)


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
    print(cmdtxt + "#" + str(ctx.message.channel) + " - " +
          str(ctx.author) + "> " + str(ctx.message.content) + reset)
    try:
        image = ctx.message.attachments[0]
    except:
        await ctx.send("Attach a square PNG less than 4mb.")
        return
    image_data = await image.read()
    try:
        await ctx.send("Morphing...")
        response = openai.Image.create_variation(
            image_data,
            n=number,
            size="512x512"
        )
        for i in range(int(number)):
            output = response['data'][i]['url']
            await ctx.send(output)
            print(debugtxt + "Morphed!" + reset)
    except openai.error.OpenAIError as e:
        errmsg = e.error['message']
        print(errtxt + "Error: " + errmsg + reset)
        await ctx.send(errmsg)


@client.command(
    name="matrix",
    help="""
    Makes an ASCII image from a PNG.
    Detail [26-100] [High-Low]
    """
)
async def matrix(ctx, detail=50):
    if detail <= 26:
        detail = 26
    print(cmdtxt + "#" + str(ctx.message.channel) + " - " +
          str(ctx.author) + "> " + str(ctx.message.content) + reset)
    try:
        image = ctx.message.attachments[0]
    except:
        await ctx.send("Attach a PNG.")
        return
    image = await image.read()
    im = Image.open(BytesIO(image))
    # Convert the image to grayscale
    im = im.convert("L")
    # Resize the image to fit the desired width
    desired_width = 40
    width, height = im.size
    aspect_ratio = height/width
    new_height = int(desired_width * (aspect_ratio/2))
    im = im.resize((desired_width, new_height))
    # Iterate over the pixels in the image
    ascii_art = ""
    for y in range(new_height):
        for x in range(desired_width):
                # Get the pixel value (0-255)
            pixel = im.getpixel((x, y))
            # Map the pixel value to an ASCII character
            # You can use any set of characters that you want
            ascii_char = " .:-=+*#%@"[pixel // int(detail)]
            ascii_art += ascii_char
        ascii_art += "\n"
    print(ascii_art)
    backtick = "`"
    ascii_art = f"{backtick}\n{ascii_art}{backtick}"
    await ctx.send(ascii_art)


@client.event
async def on_ready():
    print(debugtxt + 'Logged in as' + reset)
    print(cmdtxt + str(client.user.name) + reset)
    print(cmdtxt + str(client.user.id) + reset)
    print(debugtxt + '------' + reset)


@client.event
async def on_message(message):
    # Ignore own self
    if message.author == client.user:
        return
    # Process bot commands
    await client.process_commands(message)
    # I was mentioned
    if client.user in message.mentions:
        # This is a reply
        if message.reference is not None:
            reply = await message.channel.fetch_message(message.reference.message_id)
            reply_content = reply.content
            # Remove URLs. They break the bot.
            cleaned = re.findall(r"https?://[^\s]+", reply_content)
            # Replace the links with an empty string
            for link in cleaned:
                reply_content = reply_content.replace(link, "")
            print(chattxt + "> Re: " + str(reply.author) + "> " +
                  reply_content + reset)
            # hacky way to give bot cheap short term memory
            # Guide the conversation
            if reply.author == client.user:
                prompt = ("You said " + repr(reply_content) +
                          ", and I said: " +
                          repr(message.content))
            else:
                prompt = (str(reply.author) + " said " +
                          repr(reply_content) +
                          ", and I said: " +
                          repr(message.content))
            if reply_content == "":
                prompt = str(message.content)
        else:
            prompt = str(message.content)
        print(chattxt + "> #" + str(message.channel) + " - " +
              str(message.author) + "> " +
              str(message.content) + reset)
        try:
            response = openai.Completion.create(
                  model="text-davinci-003",
                  prompt=prompt,
                  max_tokens=2000,
                  temperature=1,
                  presence_penalty=-2,
                  frequency_penalty=2
                  )
            output = response['choices'][0]['text']
            print(chattxt + "> Response: " + output + reset + '\n')
            await message.channel.send(output)
            return
        except openai.error.OpenAIError as e:
            errmsg = e.error['message']
            print(errtxt + "Error: " + errmsg + reset)
            await message.channel.send(errmsg)

client.run(token)
