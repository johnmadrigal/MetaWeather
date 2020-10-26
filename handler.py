import json
import datetime
import requests
import csv


def endpoint(event, context):
  # csvfile = open('locations.csv')
  # location_reader = csv.reader(csvfile, delimiter=',')
  # dict_reader = csv.DictReader(csvfile)
  # locations = []
  # for row in dict_reader:
  #   locations.(row['Location'])
  # print('Locations:', locations)
  # for row in location_reader:
  #   print('row', row[0])
  # print('read', read)
  # print('event', event)
  # print('context', context)
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
  
  test_forecast = Forecast('10-26-2020', 20.57, 'Heavy Cloud')
  print('testing', test_forecast.date)


  for row in consolidated_weather:
    day = {}
    for value in weather_dict:
      day[value] = row[value]
    results[location].append(day)
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