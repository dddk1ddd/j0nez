# j0nez v.011c
OpenAI ChatGPT Discord Bot
www.phatkid.art

Responds to mentions with normal conversation through ChatGPT.
Generates AI Images in chat from prompts using DALL-E.
Morphs images into specified number of iterations.
Combines an image and an image mask to create new images from prompt.
Minimalist Help system.

Getting Started:
Create a file called '.env' in the folder with j0nez.py.
The file should only contain these two lines:

TOKEN='YOUR_BOT_TOKEN'
KEY='YOUR_API_KEY'

Replace YOUR_BOT_TOKEN with your Discord Bot Token.
Replace YOUR_API_KEY with your OpenAI API Key.

Both can be obtained from their respective developer portals.

Usage:
Commands start with '!'.
Images should be square and less than 4mb.

!image <description>
Generates a 512x512 image from a prompt.

!morph <number>
Morphs an image up to 10 times.
Works best with images generated with !image.

!remix <prompt> <image> <mask>
prompt
A text description of the desired images.
image
The image to edit. Must be a valid PNG file,
less than 4MB, and square. Works best with images from !image.
mask
An additional image whose fully transparent areas indicate
where image should be edited. Must be a valid PNG file,
less than 4MB, and have the same dimensions as image.
Included in the archive is mask.png for testing.

From ChatGPT:
"Phat Kid is an experimental electronic music artist who has a diverse 
and eclectic style that incorporates elements of various genres, including 
hip hop, techno, and ambient music. His music is characterized by its experimental 
and unconventional approach, and he often uses unconventional instruments and production 
techniques to create unique and experimental sounds. Phat Kid's music is highly 
experimental and often incorporates elements of improvisation and chance, making 
each of his performances and recordings unique. His music is often described as 
being abstract and avant-garde, and it explores a wide range of themes and emotions."
