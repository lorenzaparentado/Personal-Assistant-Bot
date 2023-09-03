import discord
from discord.ext import commands, tasks
from itertools import cycle
import os
import asyncio
import random

# Discord Intents
client = commands.Bot(command_prefix = '!', intents = discord.Intents.all())

# Starts Discord bot
@client.event
async def on_ready():
    print("Bot is connected to Discord!")
    change_status.start()

# Changes the status of the bot over 5 seconds
bot_status = cycle(["Try !ping", "Try !8", "Try !hello"])
@tasks.loop(seconds=5)
async def change_status():
    status = next(bot_status)
    await client.change_presence(activity=discord.Game(status))

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with client:
        await load()
        await client.start('MTE0NzIwMDQ5ODkxNTYxMDY1NA.Gn8lQr.Yzf2IHzfz4qnQGAcGLA0mNHPOwQCipb-x1oud0')

asyncio.run(main())



    

