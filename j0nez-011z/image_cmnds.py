from PIL import Image
from io import BytesIO
import openai
from discord.ext import commands
from formatting import errtxt, debugtxt, reset


class ImageCommands(commands.Cog):
    @commands.command(
        name="image",
        help="""
        Generate image from a description.
        """
    )
    async def image(self, ctx, *, description=''):
        prompt = ' '.join(description)
        try:
            await ctx.send("Working...")
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="256x256"
            )
            output = response['data'][0]['url']
            await ctx.send(output)
            print(debugtxt + "Image Generated!" + reset)
        except openai.error.OpenAIError as e:
            errmsg = e.error['message']
            print(errtxt + "Error: " + errmsg + reset)
            await ctx.send(errmsg)

    @commands.command(
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
    async def remix(self, ctx):
        prompt = ctx.message.content
        try:
            image = ctx.message.attachments[0]
            image_data = await image.read()
            mask = ctx.message.attachments[1]
            mask_data = await mask.read()
        except not ctx.message.attachments[0]:
            await ctx.send("Attach two square PNG files less than 4MB each.")
            return
        try:
            await ctx.send("Remixing...")
            response = openai.Image.create_edit(
                image_data,
                mask_data,
                prompt=prompt,
                n=1,
                size="256x256"
            )
            output = response['data'][0]['url']
            await ctx.send(output)
            print(debugtxt + "Remixed!" + reset)
        except openai.error.OpenAIError as e:
            errmsg = e.error['message']
            print(errtxt + "Error: " + errmsg + reset)
            await ctx.send(errmsg)

    @commands.command(
        name="morph",
        help="""
        Morphs an image [number] of times,
        with a maximum of 10.
        Must be a square PNG less than 4MB.
        Works best with images from !image.
        """
    )
    async def morph(self, ctx, number=1):
        # This is a reply
        # Todo: get image from reply
        if ctx.message.reference is not None:
            print("REPLY MORPH")
            reply = await ctx.message.channel.fetch_message(ctx.message.reference.message_id)
            try:
                image = reply.attachments[0]
            except not reply.attachments[0]:
                await ctx.send("Attach a square PNG less than 4mb.")
                return
        else:
            try:
                image = ctx.message.attachments[0]
            except not ctx.message.attachments[0]:
                await ctx.send("Attach a square PNG less than 4mb.")
                return
        image_data = await image.read()
        try:
            await ctx.send("Morphing...")
            response = openai.Image.create_variation(
                image_data,
                n=number,
                size="256x256"
            )
            for i in range(int(number)):
                output = response['data'][i]['url']
                await ctx.send(output)
                print(debugtxt + "Morphed!" + reset)
        except openai.error.OpenAIError as e:
            errmsg = e.error['message']
            print(errtxt + "Error: " + errmsg + reset)
            await ctx.send(errmsg)

    @commands.command(
        name="matrix",
        help="""
        Makes an ASCII image from a PNG.
        Detail [26-100] [High-Low]
        """
    )
    async def matrix(self, ctx, detail=50):
        if detail <= 26:
            detail = 26
        try:
            image = ctx.message.attachments[0]
        except not ctx.message.attachments[0]:
            await ctx.send("Attach a PNG.")
            return
        image = await image.read()
        im = Image.open(BytesIO(image))
        # Convert the image to grayscale
        im = im.convert("L")
        # Resize the image to fit the desired width
        desired_width = 40
        width, height = im.size
        aspect_ratio = height / width
        new_height = int(desired_width * (aspect_ratio / 2))
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


async def setup(client):
    await client.add_cog(ImageCommands(client))
