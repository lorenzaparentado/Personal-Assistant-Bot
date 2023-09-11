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

'''
    now = datetime.datetime.now()
    target = now.replace(hour= 11, minute= 36, second= 0, microsecond= 0)

    if now > target:
        target += datetime.timedelta(days=1)

    delay = (target - now).total_seconds()
    daily_message.start(delay)


@tasks.loop(hours=24)
async def daily_message():
    user = client.get_user(227143618085781504)
    if user:
        ctx = await client.get_context(user.message('!weather Philadelphia'))
        await client.invoke(ctx)
'''
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



    

