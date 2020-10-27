import json
import datetime
import requests
import csv
import asyncio
import aiohttp

def endpoint(event, context):
  csvfile = open('locations.csv')
  dict_reader = csv.DictReader(csvfile)

  locations = []
  for row in dict_reader:
    locations.append(row['Location'])

  queries = []
  for location in locations:
    query = location.replace(' ', '%20')
    queries.append(query)

  async def fetch(session, url):
    async with session.get(url) as response:
      json_response = await response.json()
      return json_response


  # URL = 'https://www.metaweather.com/api/location/search/?query=Los%20Angeles'
  
  async def gather():
    async with aiohttp.ClientSession() as session:
      # data = fetch(session, URL)
      fetch_locations = []
      
      for q in queries:
        query_location = f'https://www.metaweather.com/api/location/search/?query={q}'
        fetch_locations.append(fetch(session, query_location))
      
      data = await asyncio.gather(*fetch_locations)
      
      weathers = []

      for row in data:
        woeid = str(row[0]['woeid'])
        query_weather = f'https://www.metaweather.com/api/location/{woeid}/'
        weathers.append(fetch(session, query_weather))
      
      weather_data = await asyncio.gather(*weathers)

      class Forecast:
        def __init__(self, date, temp, description):
          self.date = date
          self.temp = temp
          self.description = description

      print('location', len(locations))
      print('weather', len(weather_data))
      results = {}
      # print(weather_data)
      # consolidated_weather = weather_data['consolidated_weather']
      # print(consolidated_weather)
      for location, city in zip(locations, weather_data):
        results[location] = []
        weather = city['consolidated_weather']
        for day in weather:
          date = day['applicable_date']
          temp = day['the_temp']
          description = day['weather_state_name']
          forecast = Forecast(date, temp, description)
          results[location].append(forecast)
          
      body = json.dumps(results)
      print(body)

      


  # weather = requests.get('https://www.metaweather.com/api/location/%s/' % woeid).text

      # print('data', data)
      # tasks = [fetch(session,URL) for _ in range(5)]
      # tests = await asyncio.gather(*tasks)
      # print('tests', tests)

  asyncio.run(gather())

  # location = 'Los%Angeles'
  # request = requests.get('https://www.metaweather.com/api/location/search/?query=Los%20Angeles').text
  # data = json.loads(request)
  # woeid = str(data[0]['woeid'])
  # weather = requests.get('https://www.metaweather.com/api/location/%s/' % woeid).text
  # weather_data = json.loads(weather)
  # consolidated_weather = weather_data['consolidated_weather']
  # weather_dict = ["applicable_date", "weather_state_name", "the_temp"]
  # results = {}
  # results[location] = []


  

  

  


  current_time = datetime.datetime.now().time()
  body = {
    "message": "Goodbye, the current time is " + str(current_time)
  }

  response = {
    "statusCode": 200,
    "body": json.dumps(body)
  }
  return response