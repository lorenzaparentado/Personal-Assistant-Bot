import discord
from discord.ext import commands
import random

class Eight_Ball(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("eightBall.py ready!")

    @commands.command(aliases=["8ball","eight_ball","eight ball", "8 ball", "8"])
    async def eightball(self, ctx, *, question):
        with open("responses.txt", "r") as f:
            random_responses = f.readlines()
            response = random.choice(random_responses)

        await ctx.send(response)

async def setup(client):
    await client.add_cog(Eight_Ball(client))
