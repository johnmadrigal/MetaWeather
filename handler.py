import json
import asyncio
import aiohttp
from utils import fetch, get_csv_column, get_s3_file
from weather import Forecast

BUCKET_NAME = 'primelocations'
OBJECT_NAME = 'locations.csv'

def endpoint(event, context):
    # get file from s3
    csv_file = get_s3_file(BUCKET_NAME, OBJECT_NAME)

    # get locations from csv
    locations = get_csv_column(csv_file, 'Location')

    # query api based on locations
    location_queries = []
    for location in locations:
        query_string = location.replace(' ', '%20')
        location_query = f'https://www.metaweather.com/api/location/search/?query={query_string}'
        location_queries.append(location_query)

    # main section for api calls to get 5 day forecast for locations
    async def main(future):
        async with aiohttp.ClientSession() as session:

            # get location data from api
            fetch_locations = [fetch(session, url) for url in location_queries]
            location_data = await asyncio.gather(*fetch_locations)

            # get weather data based of woeids
            weather_queries = []
            for row in location_data:
                woeid = str(row[0]['woeid'])
                weather_query = f'https://www.metaweather.com/api/location/{woeid}/'
                weather_queries.append(weather_query)

            fetch_weathers = [fetch(session, url) for url in weather_queries]
            weather_data = await asyncio.gather(*fetch_weathers)

            # create json object from locations and weather data
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

    # set and run event loop to complete async calls
    # store final result in body
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    future = asyncio.Future()
    task = asyncio.ensure_future(main(future))
    body = loop.run_until_complete(task)
    loop.close()

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response

