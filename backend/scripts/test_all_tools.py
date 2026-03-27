import os
import sys
from pathlib import Path

# Add backend directory to path so relative imports work
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.tools.yield_tool import YieldPredictionInternalTool
from app.tools.crop_tool import CropRecommendationInternalTool
from app.tools.fertilizer_tool import FertilizerPredictionTool
from app.tools.rain_fall import RainfallPredictionTool
from app.tools.weather_tool import WeatherInfoTool
from app.tools.soil_tool import SoilInfoTool
from app.tools.general_info_tool import ExternalKnowledgeSearchTool
from app.tools.farm_advice_tool import FarmPracticeRAGTool
from app.tools.goverment_schema_tool import GovSchemeRAGTool

def run_tests():
    # Setup output directory and file
    output_dir = Path("tooltesting")
    output_dir.mkdir(exist_ok=True)
    out_file = output_dir / "tool_test_results.txt"
    
    tools_to_test = [
        (YieldPredictionInternalTool(), {"crop": "rice", "area": 1.5, "season": "Kharif"}),
        (CropRecommendationInternalTool(), {"soil_type": "alluvial", "budget": "medium"}),
        (FertilizerPredictionTool(), {"crop": "wheat", "soil_type": "loamy"}),
        (RainfallPredictionTool(), {"location": "Pune", "month": "July"}),
        (WeatherInfoTool(), {"location": "Nagpur"}),
        (SoilInfoTool(), {"location": "Nashik"}),
        (ExternalKnowledgeSearchTool(), {"query": "latest farming techniques for cotton"}),
        (FarmPracticeRAGTool(), {"user_query": "how to control pests in sugarcane"}),
        (GovSchemeRAGTool(), {"user_query": "subsidy for drip irrigation"})
    ]

    with open(out_file, "w", encoding="utf-8") as f:
        f.write("=== KRISHI DRISTI TOOL TESTS ===\n\n")
        
        for tool, test_args in tools_to_test:
            f.write(f"--- Testing {tool.name} ---\n")
            f.write(f"Description: {tool.description}\n")
            f.write(f"Test Args: {test_args}\n")
            
            try:
                # Most LangChain BaseTools can be invoked with a dict or string
                # We'll try invoke first
                result = tool.invoke(test_args)
                f.write("Status: SUCCESS\n")
                f.write(f"Result:\n{result}\n")
            except Exception as e:
                f.write("Status: FAILED\n")
                f.write(f"Error: {str(e)}\n")
            
            f.write("\n" + "="*50 + "\n\n")

    print(f"All tests finished. Check results in: {out_file.absolute()}")

if __name__ == "__main__":
    run_tests()
