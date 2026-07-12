from fastapi import APIRouter, HTTPException
import aiohttp

router = APIRouter(
    prefix="/weather",
    tags=["weather & Utility"]
)

@router.get("/")
async def get_weather(city: str):
    city_url=f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=de"

    async with aiohttp.ClientSession() as session:
        async with session.get(city_url) as resp:
            city_data = await resp.json()

        if not city_data.get("results"):
            raise HTTPException(status_code=404, detail=f"Place '{city}' not found")

        location = city_data["results"][0]
        lat = location["latitude"]
        lon = location["longitude"]
        city_name = location["name"]

        weather_url=f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,apparent_temperature,weather_code"

        async with aiohttp.ClientSession() as weather_session:
            async with weather_session.get(weather_url) as weather_resp:
                weather_data = await weather_resp.json()

        current_weather= weather_data["current"]

        return {
            "city": city_name,
            "temperature": current_weather["temperature_2m"],
            "feels_like": current_weather["apparent_temperature"],
            "weather_code": current_weather["weather_code"]
        }


