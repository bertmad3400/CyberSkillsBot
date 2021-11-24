#!/usr/bin/python3

import discord
import random
from pathlib import Path
import requests
import json

token = Path("./token.secret").read_text()

client = discord.Client()

helpMessage = discord.Embed(title="Help page for the CyberSkills Event Bot", color=0x00ff00)
helpMessage.set_thumbnail(url="https://bertmad.dk/div/images/cyberskills.jpg")
helpMessage.add_field(name="To get the event for the current month:", value="!cs current")
helpMessage.add_field(name="To get the upcomming events", value="!cs next [number of events]")
helpMessage.add_field(name="To get the events for a specific month and year", value="!cs next (year) (month in english)")

async def getNextEvents(command):
    numberOfEvents = command.split(" ")[-1]

    if not numberOfEvents.isnumeric():
        numberOfEvents = 3

    return requests.get(f"https://bertmad.dk/api/cyberskills/nextEvents/{str(numberOfEvents)}/")

async def getEventsOfThisMonth():
    return requests.get("https://bertmad.dk/api/cyberskills/currentEvents/")

async def getEventsForSpecificMonth(command):
    month = command.split(" ")[-1]
    year = command.split(" ")[-2]

    return requests.get(f"https://bertmad.dk/api/cyberskills/{year}/{month.capitalize()}/")

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
            events = await getEventsOfThisMonth()
        elif "specific" in messageContents:
            events = await getEventsForSpecificMonth(messageContents)
        elif "help" in messageContents or messageContents == "!cs":
            await message.channel.send(embed=helpMessage)
            return
        else:
            return

        try:
            events = events.json()
        except:
            await message.channel.send(f"Your request couldn't be processed, encountered following error when hitting the API: '{events}: {events.content.decode('utf-8')}'")
            return

        embedMessages = await formatMessage(events)
        for embedMessage in embedMessages:
            await message.channel.send(embed=embedMessage)

        return

    else:
        return


client.run(token)
