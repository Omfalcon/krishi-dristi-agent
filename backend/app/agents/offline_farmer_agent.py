# import os
# from dotenv import load_dotenv
# from langchain.messages import HumanMessage
# from langchain.agents import create_agent
# from langgraph.checkpoint.sqlite import SqliteSaver
# from langchain_ollama import ChatOllama

# from app.tools.crop_tool import get_crop_prediction
# from app.tools.fertilizer_tool import get_fertilizer_prediction
# from app.tools.rain_fall import get_rainfall
# from app.tools.weather_tool import get_weather_data

# load_dotenv()

# TOOLS = [
#     get_crop_prediction,
#     get_fertilizer_prediction,
#     get_rainfall,
#     get_weather_data,
# ]


# def get_offline_llm(model_name: str = "gemma3:270m"):
#     return ChatOllama(
#         model=model_name,
#         temperature=0.3,
#     )


# def get_system_prompt(expertise_level: str = "beginner") -> str:
#     base = (
#         "You are an expert Indian Agriculture Advisor. "
#         "You must use the available tools whenever they help answer the user query. "
#         "Do not guess when a tool can provide the answer. "
#         "Give practical, short, farmer-friendly answers."
#     )
#     if expertise_level == "beginner":
#         return f"{base} Explain in simple language without asking for extra input."
#     return base


# def create_farmer_agent(llm, checkpointer: SqliteSaver):
#     return create_agent(
#         model=llm,
#         tools=TOOLS,
#         system_prompt=get_system_prompt("beginner"),
#         checkpointer=checkpointer,
#     )


# if __name__ == "__main__":
#     DB_PATH = "farmer_data.db"

#     with SqliteSaver.from_conn_string(DB_PATH) as checkpointer:
#         llm = get_offline_llm("qwen2.5:3b")
#         agent = create_farmer_agent(llm, checkpointer)

#         print("🌾 Offline Farmer AI Ready! (Tool calling enabled)")
#         print(f"📦 Database: {DB_PATH}\n")

#         while True:
#             current_user = input("Enter User ID (e.g., user1): ").strip()
#             if not current_user:
#                 print("User ID cannot be empty.")
#                 continue

#             user_query = input(f"[{current_user}] You: ").strip()
#             if user_query.lower() in ["exit", "quit"]:
#                 print("Goodbye! 🌱")
#                 break

#             try:
#                 config = {"configurable": {"thread_id": current_user}}
#                 response = agent.invoke(
#                     {"messages": [HumanMessage(content=user_query)]},
#                     config=config
#                 )
#                 last_message = response["messages"][-1]
#                 print(f"Agent: {last_message.content}\n")

#             except Exception as e:
#                 print(f"❌ Error: {e}\n")



import os
from dotenv import load_dotenv
from langchain.messages import HumanMessage
from langchain.agents import create_agent
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_ollama import ChatOllama
from langchain.tools import tool

load_dotenv()

# -----------------------------
# DUMMY TOOL DEFINITIONS
# -----------------------------
@tool
def get_crop_prediction() -> str:
    """
    Dummy crop prediction tool.
    Returns a fixed recommendation for testing.
    """
    return "Recommended crops for this region: Sugarcane, Cotton."

@tool
def get_fertilizer_prediction() -> str:
    """
    Dummy fertilizer prediction tool.
    Returns a fixed fertilizer recommendation.
    """
    return "Suggested fertilizer: 50kg Nitrogen + 30kg Phosphorous per hectare."

@tool
def get_rainfall() -> str:
    """
    Dummy rainfall tool.
    Returns a fixed rainfall value.
    """
    return "Average rainfall for this location: 120mm."

@tool
def get_weather_data() -> str:
    """
    Dummy weather tool.
    Returns a fixed weather status.
    """
    return "Current weather: 28°C, high humidity."

# -----------------------------
# TOOL LIST
# -----------------------------
TOOLS = [
    get_crop_prediction,
    get_fertilizer_prediction,
    get_rainfall,
    get_weather_data,
]

# -----------------------------
# OFFLINE LLM SETUP
# -----------------------------
def get_offline_llm(model_name: str = "lfm2.5-thinking:latest"):
    """
    Returns a lightweight offline LLM for mobile testing.
    """
    return ChatOllama(
        model=model_name,
        temperature=0.3,
        streaming=True
    )

# -----------------------------
# SYSTEM PROMPT
# -----------------------------

ZERO_SHOT_TOOL_EXAMPLES = """
Example 1:
Q: Which crop is best for my red soil?
Tools to use: get_crop_prediction

Example 2:
Q: How much fertilizer should I use for maize?
Tools to use: get_fertilizer_prediction

Example 3:
Q: What is the current rainfall?
Tools to use: get_rainfall

Example 4:
Q: Will it rain tomorrow?
Tools to use: get_weather_data

Example 5:
Q: I want to plant sugarcane and know fertilizer and weather info.
Tools to use: get_crop_prediction, get_fertilizer_prediction, get_weather_data
"""

def get_system_prompt(expertise_level="beginner") -> str:
    base = (
        "You are an expert Indian Agriculture Advisor. "
        "Use the available tools automatically when they help answer the user query. "
        "Do not guess when a tool can provide the answer. "
        "Give practical, short, farmer-friendly answers.\n\n"
        "Follow these examples to decide which tool(s) to call:\n"
        f"{ZERO_SHOT_TOOL_EXAMPLES}\n"
    )
    if expertise_level == "beginner":
        return base + "Explain in simple language without asking for extra input."
    return base

# def get_system_prompt(expertise_level: str = "beginner") -> str:
#     base = (
#         "You are an expert Indian Agriculture Advisor. "
#         "Use the available tools automatically when they help answer the user query. "
#         "Do not guess when a tool can provide the answer. "
#         "Give practical, short, farmer-friendly answers."
#     )
#     if expertise_level == "beginner":
#         return f"{base} Explain in simple language without asking for extra input."
#     return base

# -----------------------------
# AGENT CREATION
# -----------------------------
def create_farmer_agent(llm, checkpointer: SqliteSaver):
    return create_agent(
        model=llm,
        tools=TOOLS,
        system_prompt=get_system_prompt("beginner"),
        checkpointer=checkpointer,
    )

# -----------------------------
# MAIN EXECUTION
# -----------------------------
if __name__ == "__main__":
    DB_PATH = "farmer_data_dummy.db"

    with SqliteSaver.from_conn_string(DB_PATH) as checkpointer:
        llm = get_offline_llm()  # Lightweight offline model
        agent = create_farmer_agent(llm, checkpointer)

        print("🌾 Offline Dummy Farmer AI Ready! (Tool calling enabled)")
        print(f"📦 Database: {DB_PATH}\n")

        while True:
            current_user = input("Enter User ID (e.g., user1): ").strip()
            if not current_user:
                print("User ID cannot be empty.")
                continue

            user_query = input(f"[{current_user}] You: ").strip()
            if user_query.lower() in ["exit", "quit"]:
                print("Goodbye! 🌱")
                break

            try:
                config = {"configurable": {"thread_id": current_user}}
                response = agent.invoke(
                    {"messages": [HumanMessage(content=user_query)]},
                    config=config
                )
                last_message = response["messages"][-1]
                print(f"Agent: {last_message.content}\n")

            except Exception as e:
                print(f"❌ Error: {e}\n")