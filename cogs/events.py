import discord
import firebase_admin
from firebase_admin import credentials, db
from discord.ext import commands
from datetime import datetime

cred = credentials.Certificate("C:\\Users\\loren\\OneDrive\\Desktop\\DiscordBot\\discord-bot-398714-firebase-adminsdk-4emt2-c0ca0e8d93.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://discord-bot-398714-default-rtdb.firebaseio.com/'
})

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Events cog ready!")

    @commands.command()
    async def events(self, ctx):
        try:
            await ctx.send("Please enter the event name:")
            event_name = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)

            await ctx.send("Please enter the date and time (YYYY-MM-DD HH:MM):")
            date_time_str = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)

            date_time = datetime.strptime(date_time_str.content, '%Y-%m-%d %H:%M')

            await ctx.send("Does the event repeat weekly? (yes/no):")
            repeat = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)
        
            event_data = {
                'date_time': date_time.strftime('%Y-%m-%d %H:%M'),
                'repeat': repeat.content.lower() == 'yes'
            }

            ref = db.reference('events')
            ref.child(event_name.content).set(event_data)


            await ctx.send(f"Event '{event_name.content}' added!")
        except Exception as e:
            print(f"Error adding event: {str(e)}")

    @commands.command()
    async def list_events(self, ctx):

        ref = db.reference('events')
        events = ref.get()

        if events:
            event_list = "\n".join(events.keys())
            await ctx.send(f"Events:\n{event_list}")
        else:
            await ctx.send("No events have been added.")

    @commands.command()
    async def tasks(self, ctx):
        today = datetime.now().date()
        tasks_today = []

        ref = db.reference('events')
        events = ref.get()

        if events:
            for event_name, event_data in events.items():
                event_date = datetime.strptime(event_data['date_time'], '%Y-%m-%d %H:%M').date()
                event_time = datetime.strptime(event_data['date_time'], '%Y-%m-%d %H:%M').time()

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
        else:
            await ctx.send("No events have been added.")


    @commands.command()
    async def delete_event(self, ctx, event_name: str):
        ref = db.reference('events')
        event_ref = ref.child(event_name)
        if event_ref.get():
            event_ref.delete()
            await ctx.send(f"Event '{event_name}' has been deleted.")
        else:
            await ctx.send(f"Event '{event_name}' not found in the list of events.")

async def setup(client):
    await client.add_cog(Events(client))
