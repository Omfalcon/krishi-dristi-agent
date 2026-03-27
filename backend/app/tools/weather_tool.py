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




# from langchain.tools import tool
# from app.services.weather_service import get_weather_data 


# @tool
# def get_weather_info() -> str:
#     """
#     Use this tool to get weather information for the farmer's location.
#     Do NOT ask the user for weather parameters. Location is handled internally.
#     """

#     # ✅ Replace with dynamic location later
#     lat = 28.6139
#     lon = 77.2090


#     try:
#         data = get_weather_data(lat, lon)
#         return data
#     except Exception as e:
#         return f"Unable to fetch weather data right now."

# print(get_weather_info())


from typing import Type
from pydantic import BaseModel

from langchain.tools import BaseTool
from app.services.weather_service import get_weather_data


# ✅ Empty schema (no user input required)
class EmptyInput(BaseModel):
    pass


class WeatherInfoTool(BaseTool):
    name: str = "weather_data_internal"
    description: str = (
        "Fetches weather information (temperature, humidity, etc.) for the farmer's location. "
        "Does NOT require user input. "
        "Use this when current weather conditions are needed."
    )
    args_schema: Type[BaseModel] = EmptyInput

    def _run(self) -> str:
        # ✅ Hardcoded location (can replace later)
        lat = 28.6139
        lon = 77.2090

        try:
            data = get_weather_data(lat, lon)

            return (
                "🌤️ Weather Report:\n"
                f"- Location: ({lat}, {lon})\n\n"
                f"👉 Weather Details:\n{data}"
            )

        except Exception as e:
            return f"❌ Unable to fetch weather data: {str(e)}"

    async def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async not implemented")
