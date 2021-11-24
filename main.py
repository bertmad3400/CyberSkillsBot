#!/usr/bin/python3

import discord
import random
from pathlib import Path
import requests
import json

token = Path("./token.secret").read_text()

client = discord.Client()

async def getNextEvents(command):
    numberOfEvents = command.split(" ")[-1]

    if not numberOfEvents.isnumeric():
        numberOfEvents = 3

    return requests.get(f"https://bertmad.dk/api/cyberskills/nextEvents/{str(numberOfEvents)}/").json()

async def getEventsOfThisMonth():
    return requests.get("https://bertmad.dk/api/cyberskills/currentEvents/")

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
