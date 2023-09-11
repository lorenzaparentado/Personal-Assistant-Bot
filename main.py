import discord
from discord.ext import commands, tasks
from itertools import cycle
import os
import asyncio
import random
import datetime

# Discord Intents
client = commands.Bot(command_prefix = '!', intents = discord.Intents.all())

# Starts Discord bot
@client.event
async def on_ready():
    print("Bot is connected to Discord!")
    change_status.start()

events = {}

@client.command
async def events(ctx):
    await ctx.send("Please enter the event name:")
    
    def check(message):
        return message.author == ctx.author and ctx.channel == message.channel

    try:
        event_name = await client.wait_for('message', check=check, timeout=60.0)
        await ctx.send("Please enter the event date and time (e.g., 2023-09-15 14:30):")
        event_datetime = await client.wait_for('message', check=check, timeout=60.0)
        await ctx.send("Does this event repeat? (yes/no):")
        event_repeats = await client.wait_for('message', check=check, timeout=60.0)

        # Store the event in the dictionary
        events[event_name.content] = {
            'datetime': event_datetime.content,
            'repeats': event_repeats.content.lower() == 'yes'
        }

        await ctx.send("Event added successfully!")

    except asyncio.TimeoutError:
        await ctx.send("Event creation timed out. Please try again later.")

# Changes the status of the bot over 5 seconds
bot_status = cycle(["Try !ping", "Try !8", "Try !hello", "Try !weather"])
@tasks.loop(seconds=5)
async def change_status():
    status = next(bot_status)
    await client.change_presence(activity=discord.Game(status))


# Loads all of the cogs
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

# Loads client
async def main():
    async with client:
        await load()
        await client.start('MTE0NzIwMDQ5ODkxNTYxMDY1NA.Gn8lQr.Yzf2IHzfz4qnQGAcGLA0mNHPOwQCipb-x1oud0')


asyncio.run(main())



    

