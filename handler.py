import json
import csv
import boto3
import codecs
import asyncio
import aiohttp
from utils import fetch, get_csv_column
from weather import Forecast


def endpoint(event, context):
    # connect to s3
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('primelocations')
    stream = bucket.Object('locations.csv').get()["Body"]
    csv_file = codecs.getreader("utf-8")(stream)

    # get locations from csv
    locations = get_csv_column(csv_file, 'Location')

    # develop appropriate query string locations
    queries = []
    for location in locations:
        query_string = location.replace(' ', '%20')
        query_location = f'https://www.metaweather.com/api/location/search/?query={query_string}'
        queries.append(query_location)

    async def gather(future):
        async with aiohttp.ClientSession() as session:

            # get location data from api
            fetch_locations = []
            for query in queries:
                fetch_locations.append(fetch(session, query))
            location_data = await asyncio.gather(*fetch_locations)

            # get weather data based of woeids
            weathers = []
            for row in location_data:
                woeid = str(row[0]['woeid'])
                query_weather = f'https://www.metaweather.com/api/location/{woeid}/'
                weathers.append(fetch(session, query_weather))
            weather_data = await asyncio.gather(*weathers)



            # create json object from weather data
            results = {}
            for location, city in zip(locations, weather_data):
                results[location] = []
                weather = city['consolidated_weather']
                for day in weather:
                    date = day['applicable_date']
                    temp = day['the_temp']
                    description = day['weather_state_name']
                    forecast = Forecast(date, temp, description)
                    results[location].append(forecast)
        return results

    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    future = asyncio.Future()
    task = asyncio.ensure_future(gather(future))
    body = loop.run_until_complete(task)
    loop.close()


    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response
