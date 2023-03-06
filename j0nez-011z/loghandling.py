from formatting import errtxt, cmdtxt, chattxt, reset
import logging
import logging.handlers as handlers

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
logging.getLogger('discord.http').setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s', '%Y-%m-%d %H:%M:%S')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

file_handler = handlers.RotatingFileHandler('j0nez.log', maxBytes=8192, backupCount=6)
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


async def do_log(message, msgtype):
    channel = message.channel.name
    author_name = message.author.name
    author_discriminator = message.author.discriminator
    guild = message.guild.name
    content = message.content
    typecolor = ""
    if msgtype == "chat ":
        typecolor = chattxt
    elif msgtype == "error":
        typecolor = errtxt
    elif msgtype == "cmnd ":
        typecolor = cmdtxt
    elif msgtype == "edit-" or msgtype == "edit+":
        typecolor = cmdtxt
    elif msgtype == "reply" or msgtype == "re:  ":
        typecolor = cmdtxt
    elif msgtype == "self ":
        typecolor = chattxt
    formatted_message = typecolor + " [" + msgtype + "] "\
                                    + f"${guild} #{channel} @{author_name}#{author_discriminator}: "\
                                    + f"{content} " + reset
    logger.info(formatted_message)


async def setup():
    return
