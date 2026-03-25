from langchain.messages import HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from app.agents.online_farmer_agent import get_sarvam_llm , create_farmer_agent

DB_PATH = "app/data/farmer_data.db"
#/Users/ganeshnikhil/krishi-dristi-agent/backend/app/data
# Use context manager for SQLite persistence
with SqliteSaver.from_conn_string(DB_PATH) as checkpointer:
    # Setup agent (Sarvam online LLM)
    llm = get_sarvam_llm()
    agent = create_farmer_agent(llm, checkpointer)
    print("🌾 Farmer AI Ready! (SQLite persistence enabled)\n")

    while True:
        user_id = input("Enter User ID (e.g., user1): ").strip()
        if not user_id:
            print("User ID cannot be empty.")
            continue

        query = input(f"[{user_id}] You: ").strip()
        if query.lower() in ["exit", "quit"]:
            print("Goodbye! 🌱")
            break

        try:
            # thread_id isolates each user's conversation
            config = {"configurable": {"thread_id": user_id}}
            response = agent.invoke(
                {"messages": [HumanMessage(content=query)]},
                config=config
            )
            print(f"Agent: {response['messages'][-1].content}\n")

        except Exception as e:
            print(f"❌ Error: {e}\n")