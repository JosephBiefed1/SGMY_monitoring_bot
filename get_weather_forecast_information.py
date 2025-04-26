from datetime import datetime, timezone
import aiohttp
import asyncio

async def fetch_weather_forecast():
    url = 'https://api-open.data.gov.sg/v2/real-time/api/twenty-four-hr-forecast'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data

async def get_weather_forecast():
    data = await fetch_weather_forecast()
    for i in range(3):
        start_time_str = data['data']['records'][0]['periods'][i]['timePeriod']['start']
        end_time_str = data['data']['records'][0]['periods'][i]['timePeriod']['end']
        start_time = datetime.fromisoformat(start_time_str)
        end_time = datetime.fromisoformat(end_time_str)

        # Get the current time in UTC
        current_time = datetime.now(timezone.utc)

        # Convert the current time to the same timezone as start_time and end_time
        current_time_in_tz = current_time.astimezone(start_time.tzinfo)
        # Check if the current time is between the start and end times
        if start_time <= current_time_in_tz <= end_time:
            return data['data']['records'][0]['periods'][i]['regions']['north']['text']

async def main():
    forecast = await get_weather_forecast()
    return forecast
    
if __name__ == '__main__':
    asyncio.run(main())
    