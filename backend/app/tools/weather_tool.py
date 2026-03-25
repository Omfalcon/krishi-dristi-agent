# from langchain.tools import tool
# from app.services.weather_service import get_weather_data

# from typing import Literal
# from pydantic import BaseModel, Field


# class WeatherInputSchema(BaseModel):
#     option: Literal["current", "minutely", "hourly", "daily", "alerts"] = Field(
#         ...,
#         description=(
#             "Weather data type to fetch. "
#             "'current' returns current weather conditions like temperature and humidity. "
#             "'minutely' returns minute-by-minute precipitation forecast for the next 1 hour. "
#             "'hourly' returns hourly forecast for the next 48 hours. "
#             "'daily' returns daily forecast for the next 8 days. "
#             "'alerts' returns government-issued weather warnings or alerts."
#         ),
#     )



# @tool(args_schema=WeatherInputSchema)
# def get_weather_data(option: str) -> dict:
#     """Fetch weather data by excluding selected sections."""
#     lat = 123.4
#     lon = 244.5
#     return get_weather_data(lat, lon, [option])

from langchain.tools import tool
from app.services.weather_service import get_weather_data as fetch_weather_data


@tool
def get_weather_info(option: str = "current") -> str:
    """
    Use this tool to get weather information for the farmer's location.

    The model may choose the appropriate type of weather data:
    - 'current' → current weather conditions (default)
    - 'minutely' → short-term rain forecast
    - 'hourly' → next 48 hours forecast
    - 'daily' → next 7–8 days forecast
    - 'alerts' → weather warnings

    If unsure, always use 'current'.

    Do NOT ask the user for weather parameters. Location is handled internally.
    """

    # ✅ Replace with dynamic location later
    lat = 28.6139
    lon = 77.2090

    # ✅ Safety validation
    valid_options = ["current", "minutely", "hourly", "daily", "alerts"]
    if option not in valid_options:
        option = "current"

    try:
        data = fetch_weather_data(lat, lon, [option])
        return f"Weather ({option}): {data}"
    except Exception as e:
        return f"Unable to fetch weather data right now."
    
    

"""
Value:What it removes from the response
current: "Current weather conditions (temp, humidity, etc.)."
minutely: Minute-by-minute precipitation forecast for the next 1 hour.
hourly: Hourly forecast for the next 48 hours.
daily: Daily forecast for the next 8 days.
alerts: Government-issued weather warnings/alerts.
"""
