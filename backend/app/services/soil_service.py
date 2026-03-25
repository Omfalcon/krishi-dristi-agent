import requests
import os

def fetch_soil_data() -> dict:
    """
    Fetch soil data for the farmer's polygon from AgroMonitoring API.

    Reads:
    - POLYGON_ID from environment
    - AGROMONITORING_APPID from environment

    Returns:
    - dict with keys: dt, t0, t10, moisture
    """
    polyid = os.getenv("FARM_POLYGON_ID")
    appid = os.getenv("AGROMONITORING_APPID")

    if not polyid or not appid:
        raise ValueError("Polygon ID or API key not set in environment variables.")

    url = f"http://api.agromonitoring.com/agro/1.0/soil?polyid={polyid}&appid={appid}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Unable to fetch soil data: {str(e)}")