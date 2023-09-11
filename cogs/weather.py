import discord, requests, json
from discord.ext import commands

api_key = '1b9ba5b093406df81883f5497a0fb15b'

class Weather(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Weather cog ready!")

    @commands.command()
    async def weather(self, ctx, city):
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
        response = requests.get(url)

        def toFahrenheit(kelvin):
            return ((kelvin - 273.15) * (9/5) + 32)

        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            min_temp = data['main']['temp_min']
            max_temp = data['main']['temp_max']
            desc = data['weather'][0]['description']
            formatted_temp = round(toFahrenheit(temp), 2)
            formatted_min_temp = round(toFahrenheit(min_temp), 2)
            formatted_max_temp = round(toFahrenheit(max_temp), 2)
            daily_average = round((formatted_max_temp + formatted_min_temp) / 2, 2)

            await ctx.send(f'Temperature: {formatted_temp} F')
            await ctx.send(f'Minimum: {formatted_min_temp} F')
            await ctx.send(f'Maximum: {formatted_max_temp} F')
            await ctx.send(f'Daily Average: {daily_average} F')
            await ctx.send(f'Description: {desc}')
        else:
            await ctx.send('Error fetching weather data')

async def setup(client):
    await client.add_cog(Weather(client))