import httpx


# --------------------------------------------------
# Calculator
# --------------------------------------------------

def calculator(
    operation: str,
    a: float,
    b: float,
) -> float:
    """
    Perform a basic mathematical calculation.
    """

    operation = operation.lower().strip()

    # Addition
    if operation in ["add", "+", "plus"]:
        return a + b

    # Subtraction
    if operation in ["subtract", "-", "minus"]:
        return a - b

    # Multiplication
    if operation in ["multiply", "*", "x", "×", "times"]:
        return a * b

    # Division
    if operation in ["divide", "/", "÷"]:
        if b == 0:
            raise ValueError("Cannot divide by zero.")

        return a / b

    raise ValueError(
        f"Unknown operation: {operation}"
    )

# --------------------------------------------------
# Get weather data
# --------------------------------------------------

def get_weather(city: str) -> dict:
    """
    Get current weather information for any city.

    Returns weather data on success or an error message
    if the location or weather cannot be retrieved.
    """

    try:
        # Step 1: Get the city's coordinates
        geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"

        geocoding_params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json",
        }

        response = httpx.get(
            geocoding_url,
            params=geocoding_params,
            timeout=10,
        )

        response.raise_for_status()

        location_data = response.json()
        results = location_data.get("results")

        # Step 2: Handle an unknown city
        if not results:
            return {
                "city": city,
                "error": (
                    f"Could not find the exact location '{city}'. "
                ),
            }

        # Step 3: Extract latitude and longitude
        location = results[0]
        latitude = location["latitude"]
        longitude = location["longitude"]

        # Step 4: Request current weather
        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "wind_speed_10m"
            ),
        }

        response = httpx.get(
            weather_url,
            params=weather_params,
            timeout=10,
        )

        response.raise_for_status()

        # Step 5: Extract weather data
        data = response.json()
        current = data["current"]

        weather_data = {
            "temperature": current["temperature_2m"],
            "humidity": current["relative_humidity_2m"],
            "wind_speed": current["wind_speed_10m"],
        }

        # Step 6: Return successful result
        return {
            "city": city,
            "weather": weather_data,
        }

    except Exception as error:
        # Step 7: Return a readable error
        return {
            "city": city,
            "error": (
                f"Could not retrieve weather for '{city}'. "
                f"Reason: {error}"
            ),
        }

# --------------------------------------------------
# Web search
# --------------------------------------------------

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