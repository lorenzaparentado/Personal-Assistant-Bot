import requests, json

api_key = '1b9ba5b093406df81883f5497a0fb15b'
city = input('Enter city name: ')
url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
response = requests.get(url)

def toFarenheit(kelvin):
    return ((kelvin - 273.15) * (9/5) + 32)

if response.status_code != 404:
    data = response.json()
    temp = data['main']['temp']
    min = data['main']['temp_min']
    max = data['main']['temp_max']
    desc = data['weather'][0]['description']
    print(f'Temperature: {round(toFarenheit(temp), 2)} F')
    print(f'Minimum: {round(toFarenheit(min), 2)} F')
    print(f'Maximum: {round(toFarenheit(max), 2)} F')
    print(f'Daily Average: {round((toFarenheit(max) + toFarenheit(min)) / 2, 2)} F')
    print(f'Description: {desc}')
else:
    print('Error fetching weather data')