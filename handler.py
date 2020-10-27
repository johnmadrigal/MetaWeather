import json
import csv
import asyncio
import aiohttp
import boto3

def endpoint(event, context):
  # print('event', event)
  # print('context', context)
  # s3 = boto3.resource('s3')
  # bucket = s3.Bucket('primelocations')
  # csvfile = bucket.Object('locations.csv').get()['Body'].read()
  # strings = str(csvfile, 'utf-8')
  # #open and read csv
  csvfile = open('locations.csv')
  print(csvfile)
  # dict_reader = csv.DictReader(strings)
  # print(csvfile)
  # print(dict_reader)
  #
  # #create locations list from csv
  # locations = []
  # for row in dict_reader:
  #   print(row)
    # locations.append(row['Location'])

  # print('locations', locations)
  # #develop appropriate query string locations
  # queries = []
  # for location in locations:
  #   query_string = location.replace(' ', '%20')
  #   query_location = f'https://www.metaweather.com/api/location/search/?query={query_string}'
  #   queries.append(query_location)
  #
  #
  # async def fetch(session, url):
  #   async with session.get(url) as response:
  #     json_response = await response.json()
  #     return json_response
  #
  #
  # async def gather():
  #   async with aiohttp.ClientSession() as session:
  #
  #     #get location data from api
  #     fetch_locations = []
  #     for query in queries:
  #       fetch_locations.append(fetch(session, query))
  #     location_data = await asyncio.gather(*fetch_locations)
  #
  #     #get weather data based of woeids
  #     weathers = []
  #     for row in location_data:
  #       woeid = str(row[0]['woeid'])
  #       query_weather = f'https://www.metaweather.com/api/location/{woeid}/'
  #       weathers.append(fetch(session, query_weather))
  #     weather_data = await asyncio.gather(*weathers)
  #
  #     class Forecast(dict):
  #       def __init__(self, date, temp, description):
  #         dict.__init__(self, date=date, temp=temp, description=description)
  #
  #     #create json object from weather data
  #     results = {}
  #     for location, city in zip(locations, weather_data):
  #       results[location] = []
  #       weather = city['consolidated_weather']
  #       for day in weather:
  #         date = day['applicable_date']
  #         temp = day['the_temp']
  #         description = day['weather_state_name']
  #         forecast = Forecast(date, temp, description)
  #         results[location].append(forecast)
  #   return results
  #
  #
  # body = asyncio.run(gather())

  # response = {
  #   "statusCode": 200,
  #   "body": body
  # }
  return "complete"