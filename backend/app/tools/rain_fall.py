from langchain.tools import tool
from pydantic import BaseModel
from app.services.rainfall_service import get_rainfall_data


class RainfallInputSchema(BaseModel):
    pass


@tool(args_schema=RainfallInputSchema)
def get_rainfall_prediction() -> str:
    """Use this tool to get rainfall data using internally stored location information. 
    Do not ask the user for coordinates."""
    csv_file = "/Users/ganeshnikhil/krishi-dristi-agent/backend/app/data/rain_fall_distribution.csv"   # dummy file path
    query = (28.6139, 77.2090)       # dummy coordinates

    result = get_rainfall_data(csv_file, query)
    return f"According to the coordinates, rainfall is {result}"

