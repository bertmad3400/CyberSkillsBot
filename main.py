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
helpMessage.add_field(name="To get the events for a specific month and year", value="!cs next (year) (month in english)", inline=False)
helpMessage.add_field(name="To get the event for the current month:", value="!cs current", inline=False)
helpMessage.add_field(name="To get the upcomming events", value="!cs next [number of events]", inline=False)
helpMessage.add_field(name="To use compact mode", value='Add "-c"', inline=False)
helpMessage.add_field(name="To use expand mode", value='Add "-e"', inline=False)
helpMessage.set_footer(text="By bertie#5137")

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

    return month, year, requests.get(f"https://bertmad.dk/api/cyberskills/{year}/{month.capitalize()}/")

async def formatMessage(events, inline):
    embedMessages = []
    for event in events:
        currentMessage = discord.Embed(title=event["title"], description=event["description"], url=event["eventURL"], color=0x00ff00)

        currentMessage.set_thumbnail(url=event["imageURL"])

        for eventDetail in ["date", "time", "location"]:
            currentMessage.add_field(name=eventDetail.capitalize(), value=event[eventDetail], inline=inline)

        embedMessages.append(currentMessage)

    return embedMessages

async def formatMessageCompact(events, evenType):
    currentMessage = discord.Embed(title=f"List of {evenType}", color=0x00ff00)
    currentMessage.set_thumbnail(url="https://bertmad.dk/div/images/cyberskills.jpg")

    for event in events:
        title = (event["title"][:57].strip() + "...") if len(event["title"]) > 60 else event["title"]
        currentMessage.add_field(name=f"**{event['date']}** | *{event['time']}*", value=f"[{title}]({event['eventURL']})", inline=False)

    return currentMessage

@client.event
async def on_ready():
    print(f'We have logged in as "{client.user}"')

@client.event
async def on_message(message):
    if message.content.lower().startswith("!cs") and message.author != client.user:

        if message.channel.name != "upcoming-events" and message.guild.name == "Cyber-Skills":
            return

        messageContents = message.content.lower()

        if "-c" in messageContents:
            compactMessage = 2
        elif "-e" in messageContents:
            compactMessage = 0
        else:
            compactMessage = 1

        messageContents = messageContents.replace("-c", "").replace("-e", "").strip()

        if "next" in messageContents:
            events = await getNextEvents(messageContents)
            evenType = "Upcoming Events"
        elif "current" in messageContents:
            events = await getEventsOfThisMonth()
            evenType = "Events for the Current Month"
        elif "specific" in messageContents:
            month, year, events = await getEventsForSpecificMonth(messageContents)
            evenType = f"Events for {month.capitalize()} {year}"
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

        if compactMessage == 2:
            embedMessage = await formatMessageCompact(events, evenType)
            await message.channel.send(embed=embedMessage)
        else:
            embedMessages = await formatMessage(events, bool(compactMessage))
            for embedMessage in embedMessages:
                await message.channel.send(embed=embedMessage)

        return

    return


client.run(token)
