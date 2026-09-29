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


def get_weather(latitude: float, longitude: float) -> dict:
    """
    Get current weather information for a location
    using the Open-Meteo API.
    """

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
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