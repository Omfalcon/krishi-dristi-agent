from langchain.tools import tool
from app.services.soil_service import fetch_soil_data  # core service

@tool
def get_soil_info() -> str:
    """
    Fetch soil data for the farmer's location.
    Automatically provides:
    - dt: time of data calculation (Unix time, UTC)
    - t0: surface temperature in Kelvins
    - t10: temperature at 10 cm depth in Kelvins
    - moisture: soil moisture in m³/m³
    """
    try:
        data = fetch_soil_data()
        
        dt = data.get("dt", "N/A")
        t0 = data.get("t0", "N/A")
        t10 = data.get("t10", "N/A")
        moisture = data.get("moisture", "N/A")
        
        return (
            f"Soil Data:\n"
            f"- Time (dt, UTC): {dt}\n"
            f"- Surface temperature (t0, K): {t0}\n"
            f"- Temperature at 10cm depth (t10, K): {t10}\n"
            f"- Soil moisture (m³/m³): {moisture}"
        )
    except Exception as e:
        return f"Unable to fetch soil data. Error: {e}"
