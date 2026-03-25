from langchain.tools import tool
from app.services.searxng_service import search_web
from pydantic import BaseModel, Field


class SearchInputSchema(BaseModel):
    query: str = Field(
        ...,
        description="The search query to look up on the internet."
    )

# """Use this tool ONLY as a last resort when the user asks for external, recent, or general information 
#     that is not available through internal farming tools.

#     Always prefer internal tools such as crop prediction, fertilizer recommendation, weather, and soil analysis first.

#     Do NOT use this tool for crop, fertilizer, soil, or weather queries.

#     Return only relevant and concise information from the search results.
#     """


@tool(args_schema=SearchInputSchema)
def search_external_knowledge(query: str) -> str:
    """Use only for external or latest information not covered by internal farming tools. 
Do not use for crop, fertilizer, soil, or weather queries."""
    return search_web(query)
