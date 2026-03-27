# from langchain.tools import tool
# from app.services.searxng_service import search_web
# from pydantic import BaseModel, Field


# class SearchInputSchema(BaseModel):
#     query: str = Field(
#         ...,
#         description="The search query to look up on the internet."
#     )

# # """Use this tool ONLY as a last resort when the user asks for external, recent, or general information 
# #     that is not available through internal farming tools.

# #     Always prefer internal tools such as crop prediction, fertilizer recommendation, weather, and soil analysis first.

# #     Do NOT use this tool for crop, fertilizer, soil, or weather queries.

# #     Return only relevant and concise information from the search results.
# #     """


# @tool(args_schema=SearchInputSchema)
# def search_external_knowledge(query: str) -> str:
#     """Use only for external or latest information not covered by internal farming tools. 
# Do not use for crop, fertilizer, soil, or weather queries."""
#     return search_web(query)


from typing import Type
from pydantic import BaseModel, Field

from langchain.tools import BaseTool
from app.services.searxng_service import search_web


# ✅ Input Schema
class SearchInputSchema(BaseModel):
    query: str = Field(
        ...,
        description="Search query for external or recent information from the internet"
    )


# ✅ Tool Class (Recommended for Agents)
class ExternalKnowledgeSearchTool(BaseTool):
    name: str = "external_knowledge_search"
    description: str = (
        "Use this tool ONLY for external, recent, or general knowledge queries "
        "that are not covered by internal farming tools.\n\n"
        "⚠️ STRICT RULES:\n"
        "- DO NOT use for crop, fertilizer, soil, or weather queries\n"
        "- Use only as a LAST RESORT\n"
        "- Returns concise and relevant search results"
    )
    args_schema: Type[BaseModel] = SearchInputSchema

    def _run(self, query: str) -> str:
        try:
            results = search_web(query)

            if not results:
                return "No relevant information found from external sources."

            return results

        except Exception as e:
            return f"Error while fetching external information: {str(e)}"

    async def _arun(self, query: str) -> str:
        raise NotImplementedError("Async not implemented")
    
    
    