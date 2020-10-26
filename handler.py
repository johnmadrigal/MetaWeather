import json
import datetime
import requests


def endpoint(event, context):
  request = requests.get('https://www.metaweather.com/api/location/search/?query=london')
  print(request.text)
  current_time = datetime.datetime.now().time()
  body = {
    "message": "Goodbye, the current time is " + str(current_time)
  }

  response = {
    "statusCode": 200,
    "body": json.dumps(body)
  }
  return response