from loghandling import do_log
import re
import openai

personality_active = True
personality_type = "You are a grizzled, weathered, old, retired children's entertainer," \
                   "who's had enough of making children happy, and just wants to drink himself to death. "


async def do_messages(client, message):
    # Process bot commands
    await client.process_commands(message)
    # I was mentioned
    if client.user in message.mentions:
        # set the status as typing
        async with message.channel.typing():
            try:
                # This is a reply
                if message.reference is not None:
                    reply = await message.channel.fetch_message(message.reference.message_id)
                    reply_content = reply.content
                    # Remove URLs. They break the bot.
                    cleaned = re.findall(r"https?://\S+", reply_content)
                    # Replace the links with an empty string
                    for link in cleaned:
                        reply_content = reply_content.replace(link, "")
                    await do_log(reply, "re:  ")
                    await do_log(message, "reply")
                    # hacky way to give bot cheap short term memory
                    # Guide the conversation
                    # Also inject personality
                    if reply.author == client.user:
                        if personality_active:
                            prompt = personality_type + ("You said " + repr(reply_content) +
                                                         ", and I said: " +
                                                         repr(message.content) + " You say, ")
                        else:
                            prompt = repr(message.content)
                    else:
                        if personality_active:
                            prompt = personality_type + (str(reply.author.name) + " said " +
                                                         repr(reply_content) +
                                                         ", and I said: " +
                                                         repr(message.content) + " You say, ")
                        else:
                            prompt = repr(message.content)
                    # Not a reply
                else:
                    await do_log(message, "chat ")
                    if personality_active:
                        prompt = personality_type + str(message.content)
                    else:
                        prompt = str(message.content)

                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=prompt,
                    max_tokens=1000,
                    temperature=1,
                    presence_penalty=-2,
                    frequency_penalty=2
                )
                output = response['choices'][0]['text']
                output = output.lstrip()
                await message.channel.send(output)
            except openai.error.OpenAIError as e:
                errmsg = e.error['message']
                await do_log(errmsg, "error")
                await message.channel.send(errmsg)
    else:
        if message.content.startswith(client.command_prefix):
            await do_log(message, "cmnd ")
        else:
            await do_log(message, "chat ")


async def setup():
    return
