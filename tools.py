import httpx


def calculator(operation: str, a: float, b: float) -> float:
    """
    Perform a basic mathematical calculation.
    """

    operation = operation.lower().strip()

    # Accept common variations
    if operation in ["add", "+", "plus"]:
        return a + b

    if operation in ["subtract", "-", "minus"]:
        return a - b

    if operation in ["multiply", "*", "x", "×", "times"]:
        return a * b

    if operation in ["divide", "/", "÷"]:
        if b == 0:
            raise ValueError("Cannot divide by zero.")

        return a / b

    raise ValueError(
        f"Unknown operation: {operation}"
    )


def get_coordinates(city: str) -> tuple[float, float]:
    """
    Convert a city name into latitude and longitude
    using the Open-Meteo Geocoding API.
    """

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json",
    }

    response = httpx.get(
        url,
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    results = data.get("results")

    if not results:
        raise ValueError(
            f"Could not find the location: {city}"
        )

    location = results[0]

    latitude = location["latitude"]
    longitude = location["longitude"]

    return latitude, longitude


def get_weather(latitude: float, longitude: float) -> dict:
    """
    Get current weather information for a location
    using the Open-Meteo API.
    """

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "wind_speed_10m"
        ),
    }

    response = httpx.get(
        url,
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    current = data["current"]

    return {
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "wind_speed": current["wind_speed_10m"],
    }


def web_search(
    question: str,
    api_key: str,
    model: str,
) -> str:
    """
    Search the web for current or up-to-date information
    using OpenRouter's web search.
    """

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "tools": [
            {
                "type": "openrouter:web_search"
            }
        ],
        "messages": [
            {
                "role": "user",
                "content": question,
            }
        ],
    }

    response = httpx.post(
        url,
        headers=headers,
        json=payload,
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]