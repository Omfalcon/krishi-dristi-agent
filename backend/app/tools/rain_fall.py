# from langchain.tools import tool
# from pydantic import BaseModel
# from app.services.rainfall_service import get_rainfall_data


# class RainfallInputSchema(BaseModel):
#     pass


# @tool(args_schema=RainfallInputSchema)
# def get_rainfall_prediction() -> str:
#     """Use this tool to get rainfall data using internally stored location information. 
#     Do not ask the user for coordinates."""
#     csv_file = "app/data/rain_fall_distribution.csv"   # dummy file path
#     query = (28.6139, 77.2090)       # dummy coordinates
#     result = get_rainfall_data(csv_file, query)
#     return f"According to the coordinates, rainfall is {result}"

from typing import Type
from pydantic import BaseModel
from pathlib import Path

from langchain.tools import BaseTool
from app.services.rainfall_service import get_rainfall_data


# ✅ Empty input schema (no user input required)
class EmptyInput(BaseModel):
    pass


class RainfallPredictionTool(BaseTool):
    name: str = "rainfall_prediction_internal"
    description: str = (
        "Provides rainfall data using internally stored location coordinates. "
        "Does NOT require user input. "
        "Use this when rainfall information is needed for current conditions."
    )
    args_schema: Type[BaseModel] = EmptyInput

    def _run(self) -> str:
        # ✅ Hardcoded internal data
        csv_file = str(Path(__file__).resolve().parent.parent / "data" / "rain_fall_distribution.csv")
        coordinates = (28.6139, 77.2090)  # Example: Delhi

        try:
            result = get_rainfall_data(csv_file, coordinates)

            return (
                "🌧️ Rainfall Analysis:\n"
                f"- Location Coordinates: {coordinates}\n\n"
                f"👉 Estimated Rainfall: {result}"
            )

        except Exception as e:
            return f"❌ Error while fetching rainfall data: {str(e)}"

    async def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async not implemented")
