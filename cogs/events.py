import discord
from discord.ext import commands
from datetime import datetime

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.events = {}  # Dictionary to store events

    @commands.Cog.listener()
    async def on_ready(self):
        print("Events cog ready!")

    @commands.command()
    async def events(self, ctx):
        await ctx.send("Please enter the event name:")
        event_name = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)

        await ctx.send("Please enter the date and time (YYYY-MM-DD HH:MM):")
        date_time_str = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)

        date_time = datetime.strptime(date_time_str.content, '%Y-%m-%d %H:%M')

        await ctx.send("Does the event repeat weekly? (yes/no):")
        repeat = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)
       
        self.events[event_name.content] = {
            'date_time': date_time,
            'repeat': repeat.content.lower() == 'yes'
        }

        await ctx.send(f"Event '{event_name.content}' added!")

    @commands.command()
    async def list_events(self, ctx):
        if self.events:
            event_list = "\n".join(self.events.keys())
            await ctx.send(f"Events:\n{event_list}")
        else:
            await ctx.send("No events have been added.")

    @commands.command()
    async def tasks(self, ctx):
        today = datetime.now().date()
        tasks_today = []

        for event_name, event_data in self.events.items():
            event_date = event_data['date_time'].date()
            event_time = event_data['date_time'].time()

            if event_data['repeat'] and event_date.weekday() == today.weekday():
                tasks_today.append(f"{event_name} at {event_time.strftime('%H:%M')}")
            elif event_date == today:
                tasks_today.append(f"{event_name} at {event_time.strftime('%H:%M')}")

        if tasks_today:
            await ctx.send(f"Tasks for today ({today}):")
            for task in tasks_today:
                await ctx.send(task)
        else:
            await ctx.send("No tasks for today.")

async def setup(client):
    await client.add_cog(Events(client))
