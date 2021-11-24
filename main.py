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

async def formatMessage(events):
    embedMessages = []
    for event in events:
        currentMessage = discord.Embed(title=event["title"], description=event["description"], url=event["eventURL"], color=0x00ff00)

        currentMessage.set_thumbnail(url=event["imageURL"])

        for eventDetail in ["date", "time", "location"]:
            currentMessage.add_field(name=eventDetail.capitalize(), value=event[eventDetail], inline=False)

        embedMessages.append(currentMessage)

    return embedMessages

@client.event
async def on_ready():
    print(f'We have logged in as "{client.user}"')

@client.event
async def on_message(message):
    if message.content.lower().startswith("!cs") and message.author != client.user:
        messageContents = message.content.lower()

        if "next" in messageContents:
            events = await getNextEvents(messageContents)
        elif "current" in messageContents:
            events = await getNextEvents(messageContents)
        else:
            return

        embedMessages = await formatMessage(events)
        for embedMessage in embedMessages:
            await message.channel.send(embed=embedMessage)

        return

    else:
        return


client.run(token)
