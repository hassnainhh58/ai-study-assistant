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
    Get current weather information for a city.

    Returns weather data on success or an error message
    if the city cannot be found or weather cannot be retrieved.
    """

    # Step 1: Validate the city name
    city = city.strip()

    if not city or not any(char.isalpha() for char in city):
        return {
            "success": False,
            "city": city,
            "error": "Please enter a valid city name.",
        }

    try:
        # Step 2: Find the city's coordinates
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

        # Step 3: Check whether the city was found
        if not results:
            return {
                "success": False,
                "city": city,
                "error": f"Could not find the city '{city}'.",
            }

        # Step 4: Check whether the result matches the city
        location = results[0]
        found_city = location.get("name", "")

        if found_city.casefold() != city.casefold():
            return {
                "success": False,
                "city": city,
                "error": (
                    f"Could not verify '{city}' as the returned "
                    f"location was '{found_city}'."
                ),
            }

        # Step 5: Get the city's coordinates
        latitude = location["latitude"]
        longitude = location["longitude"]

        # Step 6: Request current weather
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

        # Step 7: Extract weather data
        data = response.json()
        current = data["current"]

        weather_data = {
            "temperature": current["temperature_2m"],
            "humidity": current["relative_humidity_2m"],
            "wind_speed": current["wind_speed_10m"],
        }

        # Step 8: Return successful result
        return {
            "success": True,
            "city": city,
            "weather": weather_data,
        }

    except Exception as error:
        # Step 9: Handle errors
        return {
            "success": False,
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