#!/usr/bin/python3

import discord
import random
from pathlib import Path

token = Path("./token.secret").read_text()

client = discord.Client()

@client.event
async def on_ready():
    print(f'We have logged in as "{client.user}"')

@client.event
async def on_message(message):
    if message.content.lower().startswith("!cs") and message.authorr != client.user:
        messageContents = message.content.lower()
        return

    else:
        return


client.run(token)
