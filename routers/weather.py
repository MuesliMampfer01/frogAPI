from fastapi import APIRouter, HTTPException
import aiohttp

router = APIRouter(
    prefix="/weather",
    tags=["Weather & Utility"]
)

# WMO Wetter-Code Übersetzung ins Deutsche
WMO_WEATHER_CODES = {
    0: "Klar / Sonnig",
    1: "Leicht bewölkt",
    2: "Teilweise bewölkt",
    3: "Bedeckt",
    45: "Nebel",
    48: "Raufrostnebel",
    51: "Leichter Sprühregen",
    53: "Mäßiger Sprühregen",
    55: "Starker Sprühregen",
    61: "Leichter Regen",
    63: "Mäßiger Regen",
    65: "Starker Regen",
    71: "Leichter Schneefall",
    73: "Mäßiger Schneefall",
    75: "Starker Schneefall",
    80: "Leichter Regenschauer",
    81: "Mäßiger Regenschauer",
    82: "Starker Regenschauer",
    95: "Gewitter",
    96: "Gewitter mit Hagel",
    99: "Schweres Gewitter mit Hagel"
}

@router.get("/")
async def get_weather(city: str):
    city_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=de"

    async with aiohttp.ClientSession() as session:
        # 1. Ort suchen
        async with session.get(city_url) as resp:
            city_data = await resp.json()

        if not city_data.get("results"):
            raise HTTPException(status_code=404, detail=f"Ort '{city}' wurde nicht gefunden.")

        location = city_data["results"][0]
        lat = location["latitude"]
        lon = location["longitude"]
        city_name = location["name"]
        country = location.get("country", "")

        # 2. Wetterdaten abfragen (Aktuelle Werte + Tages-Höchst/Tiefstwerte)
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
            f"&daily=temperature_2m_max,temperature_2m_min"
            f"&timezone=auto&models=icon_seamless"
        )

        async with session.get(weather_url) as weather_resp:
            weather_data = await weather_resp.json()

        current = weather_data["current"]
        daily = weather_data["daily"]

        wmo_code = current["weather_code"]
        condition = WMO_WEATHER_CODES.get(wmo_code, "Unbekannt")

        # 3. Strukturierte Rückgabe für Discord Embeds
        return {
            "city": city_name,
            "country": country,
            "condition": condition,
            "temperature": round(current["temperature_2m"]),
            "temp_max": round(daily["temperature_2m_max"][0]),
            "temp_min": round(daily["temperature_2m_min"][0]),
            "humidity": current["relative_humidity_2m"],
            "wind_speed": round(current["wind_speed_10m"]),
            "weather_code": wmo_code
        }
