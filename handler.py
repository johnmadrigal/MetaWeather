import json
import datetime
import requests
import csv


def endpoint(event, context):
  csvfile = open('locations.csv')
  location_reader = csv.reader(csvfile, delimiter=',')
  dict_reader = csv.DictReader(csvfile)
  for row in dict_reader:
    print('Location:', row['Location'])
  # for row in location_reader:
  #   print('row', row[0])
  # print('read', read)
  # print('event', event)
  # print('context', context)
  # request = requests.get('https://www.metaweather.com/api/location/search/?query=london')
  # print(request.text)
  current_time = datetime.datetime.now().time()
  body = {
    "message": "Goodbye, the current time is " + str(current_time)
  }

  response = {
    "statusCode": 200,
    "body": json.dumps(body)
  }
  return response