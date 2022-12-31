import discord
import requests
from discord.ext import commands

# pk's chatgpt discord bot version .01
# www.phatkid.art
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

#def chatGPT(text):

@client.event
async def on_message(message):
    print("message: " + message.content)
    if client.user in message.mentions:
        # Send a message in response to the mention
        prompt = message.content[len(client.user.mention) + 1:]
        #print("prompt: " + prompt)
        url = "https://api.openai.com/v1/completions"
        headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer API", #replace API with your OpenAI API
        }
        data = {
        "model": "text-davinci-003",
        "prompt": prompt,
        "max_tokens": 4000,
        "temperature": 1.0,
        }
        response = requests.post(url, headers=headers, json=data)
        output = response.json()['choices'][0]['text']
        await message.channel.send(output)
        return #print(output)


client.run('TOKEN') #replace TOKEN with your Bot TOKEN
