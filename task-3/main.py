# Task 3
# * Integrate AbortController or other Cancelable approach

import asyncio


async def get_hourly_forecast():
    try:
        file_name = "hourly1h_zip_eu.json.gz"
        api_key = "some_api_key"
        url = f"https://bulk.openweathermap.org/snapshot/{file_name}?appid={api_key}"
        delay = 5
        await asyncio.sleep(delay)
        print("Finished downloading the forecast.")
        forecast = {
            "country": "UA",
            "city": "Kyiv",
            "temperature": "0",
            "datetime": "2024-25-12 20:00:00"
        }
        return forecast
    except asyncio.CancelledError:
        print("The forecast download was cancelled.")
        raise


async def main():
    task = asyncio.create_task(get_hourly_forecast())

    delay = 3
    await asyncio.sleep(delay)
    task.cancel()

    try:
        result = await task
        print(result)
    except asyncio.CancelledError:
        print("The task was cancelled.")

if __name__ == "__main__":
    asyncio.run(main())
