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
# Get coordinates
# --------------------------------------------------

def get_coordinates(
    city: str,
) -> tuple[float, float] | tuple[None, None]:
    """
    Convert a city name into latitude and longitude
    using the Open-Meteo Geocoding API.

    Returns (None, None) if no location is found.
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
        return None, None

    location = results[0]

    return (
        location["latitude"],
        location["longitude"],
    )


# --------------------------------------------------
# Get weather data
# --------------------------------------------------

def get_weather(city: str) -> dict:
    """
    Get current weather information for a city.

    Returns:
        success=True with weather data on success.
        success=False with an error message on failure.
    """

    try:
        # Step 1: Get city coordinates
        latitude, longitude = get_coordinates(city)

        # Step 2: Check if the city was found
        if latitude is None or longitude is None:
            return {
                "success": False,
                "city": city,
                # "error": (
                #     f"Could not find the location '{city}'. "
                # ),
            }

        # Step 3: Request current weather
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

        # Step 4: Extract weather data
        data = response.json()
        current = data["current"]

        weather_data = {
            "temperature": current["temperature_2m"],
            "humidity": current["relative_humidity_2m"],
            "wind_speed": current["wind_speed_10m"],
        }

        # Step 5: Return successful result
        return {
            "success": True,
            "city": city,
            "weather": weather_data,
        }

    except Exception as error:
        # Step 6: Return an error instead of raising it
        return {
            "success": False,
            "city": city,
            # "error": (
            #     f"Could not retrieve weather for '{city}'. "
            #     f"Reason: {error}"
            # ),
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