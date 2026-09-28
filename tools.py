#it is a tool/library your python code uses to send and recieve web requests over the internet.
import httpx

#calculator tool
def calculator(operation: str, a: float, b: float) -> float:
    """
    Perform a basic mathematical calculation.
    """

    if operation == "add":
        return a + b

    if operation == "subtract":
        return a - b

    if operation == "multiply":
        return a * b

    if operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero.")

        return a / b

    raise ValueError("Unknown operation.")

#weather tool
def get_weather(latitude: float, longitude: float) -> dict:
    """
    Get current weather information for a location
    using the Open-Meteo API.  
    """
#URL tells the program where to send the request
    url = "https://api.open-meteo.com/v1/forecast"
#parameters
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
    }
#its saying make a GET request to this URL with these parameters
#response will contain information such as status code 200,400,401,etc
    response = httpx.get(url, params=params, timeout=10)

    
#if the HTTP request failed raise an exception and if successful,execution continues
    response.raise_for_status()

    data = response.json()
#get current data
    current = data["current"]
#returning cleaner data
    return {
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "wind_speed": current["wind_speed_10m"],
    }


def get_coordinates(city: str) -> tuple[float, float]:
    """
    Convert a supported city name into latitude and longitude.
    """

    cities = {
        "islamabad": (33.6844, 73.0479),
        "lahore": (31.5204, 74.3587),
        "karachi": (24.8607, 67.0011),
        "peshawar": (34.0151, 71.5249),
        "quetta": (30.1798, 66.9750),
        "new york": (40.7128, -74.0060),
        "london": (51.5074, -0.1278),
    }

    city_key = city.lower().strip()

    if city_key not in cities:
        raise ValueError(
            f"I don't currently have coordinates for {city}."
        )

    return cities[city_key]