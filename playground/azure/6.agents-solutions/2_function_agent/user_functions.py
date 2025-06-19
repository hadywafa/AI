import json
from typing import Any, Callable, Set


def fetch_weather(location: str) -> str:
    """Fetches the weather information for the specified location.

    Args:
        location (str): The location (e.g., city name) to fetch weather for.

    Returns:
        str: A JSON string containing the weather information (e.g., '{"weather": "Sunny, 25°C"}').
    """
    # In a real-world scenario, you'd integrate with a weather API.
    # Here, we'll mock the response.
    mock_weather_data = {
        "New York": "Sunny, 25°C",
        "London": "Cloudy, 18°C",
        "Tokyo": "Rainy, 22°C",
    }
    weather = mock_weather_data.get(
        location, "Weather data not available for this location."
    )
    weather_json = json.dumps({"weather": weather})
    return weather_json


# Statically defined user functions for fast reference
user_functions: Set[Callable[..., Any]] = {
    fetch_weather,
}
