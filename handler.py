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


  URL = 'https://www.metaweather.com/api/location/search/?query=Los%20Angeles'
  
  async def gather():
    async with aiohttp.ClientSession() as session:
      data = fetch(session, URL)
      tasks = [fetch(session,URL) for _ in range(5)]
      tests = await asyncio.gather(*tasks)
      print('tests', tests)

  asyncio.run(gather())

  location = 'Los%Angeles'
  request = requests.get('https://www.metaweather.com/api/location/search/?query=Los%20Angeles').text
  data = json.loads(request)
  woeid = str(data[0]['woeid'])
  weather = requests.get('https://www.metaweather.com/api/location/%s/' % woeid).text
  weather_data = json.loads(weather)
  consolidated_weather = weather_data['consolidated_weather']
  weather_dict = ["applicable_date", "weather_state_name", "the_temp"]
  results = {}
  results[location] = []


  class Forecast:
    def __init__(self, date, temp, description):
      self.date = date
      self.temp = temp
      self.description = description

  for row in consolidated_weather:
    date = row['applicable_date']
    temp = row['the_temp']
    description = row['weather_state_name']
    forecast = Forecast(date, temp, description)
    # print('forecast', forecast)  
    results[location].append(forecast)
    # print("Date:", row["applicable_date"], "Description:", row["weather_state_name"], "Temp:", row["the_temp"])
  print(results)

  # print(weather_data)
  


  current_time = datetime.datetime.now().time()
  body = {
    "message": "Goodbye, the current time is " + str(current_time)
  }

  response = {
    "statusCode": 200,
    "body": json.dumps(body)
  }
  return response