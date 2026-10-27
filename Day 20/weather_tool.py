
import json
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import HTTPError, URLError


def weather_tool(city):
    """Retrieve current weather for a city."""

    if not isinstance(city, str) or not city.strip():
        return {"success": False, "error": "Enter a valid city name."}

    try:
        query = urlencode({
            "name": city.strip(),
            "count": 1,
            "language": "en",
            "format": "json"
        })

        with urlopen(
            f"https://geocoding-api.open-meteo.com/v1/search?{query}",
            timeout=10
        ) as response:
            locations = json.loads(response.read().decode("utf-8"))

        results = locations.get("results", [])
        if not results:
            return {"success": False, "error": "City not found."}

        location = results[0]
        query = urlencode({
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "current": (
                "temperature_2m,relative_humidity_2m,"
                "apparent_temperature,wind_speed_10m,weather_code"
            )
        })

        with urlopen(
            f"https://api.open-meteo.com/v1/forecast?{query}",
            timeout=10
        ) as response:
            weather = json.loads(response.read().decode("utf-8"))

        current = weather["current"]

        return {
            "success": True,
            "city": location.get("name", city),
            "country": location.get("country", ""),
            "temperature_c": current.get("temperature_2m"),
            "feels_like_c": current.get("apparent_temperature"),
            "humidity_percent": current.get("relative_humidity_2m"),
            "wind_speed_kmh": current.get("wind_speed_10m"),
            "weather_code": current.get("weather_code"),
            "observed_at": current.get("time")
        }

    except (HTTPError, URLError, TimeoutError, OSError) as error:
        return {"success": False, "error": f"Weather request failed: {error}"}
    except (ValueError, KeyError, TypeError) as error:
        return {"success": False, "error": f"Invalid API response: {error}"}


def display_result(result):
    print("\n" + "=" * 42)
    print("             CURRENT WEATHER")
    print("=" * 42)

    if not result["success"]:
        print(f"  Error: {result['error']}")
    else:
        print(f"  Location    : {result['city']}, {result['country']}")
        print(f"  Temperature : {result['temperature_c']} °C")
        print(f"  Feels like  : {result['feels_like_c']} °C")
        print(f"  Humidity    : {result['humidity_percent']}%")
        print(f"  Wind speed  : {result['wind_speed_kmh']} km/h")
        print(f"  Weather code: {result['weather_code']}")
        print(f"  Observed at : {result['observed_at']}")

    print("=" * 42)


if __name__ == "__main__":
    display_result(weather_tool("Mumbai"))
