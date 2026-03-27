

# import os
# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain.tools import tool
# from app.data.farming_practice import FARMCONTEXT

# load_dotenv()


# @tool
# def get_farm_practice_rag(user_query: str) -> str:
#     """
#     Provides good farming advice based on provided best practices.
#     Works in any Indian language.
#     """
#     api_key = os.getenv("SARVAM_MODEL_API")
#     model_name = os.getenv("SARVAM30_MODEL_NAME")
    
#     llm = ChatOpenAI(
#         api_key=api_key,
#         base_url="https://api.sarvam.ai/v1",
#         model=model_name,
#         temperature=0.3  # Slightly higher for conversational advice
#     )

#     prompt = ChatPromptTemplate.from_messages([
#         ("system", (
#             "You are 'Krishi Expert', a multilingual agricultural advisor.\n"
#             "FARMING KNOWLEDGE CONTEXT:\n{context}\n\n"
#             "INSTRUCTIONS:\n"
#             "1. Detect the user's language (Hindi, Marathi, etc.).\n"
#             "2. Provide a detailed, step-by-step answer in that language based ONLY on the context.\n"
#             "3. Use simple, farmer-friendly terms (e.g., 'Mitti' instead of 'Soil' in Hindi).\n"
#             "4. If the practice is not mentioned, provide general safe farming advice."
#         )),
#         ("human", "{query}"),
#     ])

#     chain = prompt | llm | StrOutputParser()
#     return chain.invoke({"context": FARMCONTEXT, "query": user_query})


import os
from typing import Type
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.tools import BaseTool

from app.data.farming_practice import FARMINGCONTEXT


load_dotenv()


# ✅ Input Schema
class FarmPracticeInput(BaseModel):
    user_query: str = Field(
        ...,
        description="Question about farming practices (e.g., irrigation, pest control, soil care)"
    )


# ✅ Reusable LLM
def get_llm():
    return ChatOpenAI(
        api_key=os.getenv("SARVAM_MODEL_API"),
        base_url="https://api.sarvam.ai/v1",
        model=os.getenv("SARVAM105_MODEL_NAME"),
        temperature=0.3
    )


# ✅ Tool Class
class FarmPracticeRAGTool(BaseTool):
    name: str = "farming_practice_advisor"
    description: str = (
        "Provides farming advice such as irrigation methods, pest control, "
        "soil management, and best agricultural practices. "
        "Responds in the user's language using farmer-friendly explanations."
    )
    args_schema: Type[BaseModel] = FarmPracticeInput

    def _run(self, user_query: str) -> str:
        llm = get_llm()

        prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "You are 'Krishi Expert', a multilingual agricultural advisor.\n"
                "FARMING KNOWLEDGE CONTEXT:\n{context}\n\n"
                "INSTRUCTIONS:\n"
                "1. Detect the user's language.\n"
                "2. Answer ONLY using the provided context.\n"
                "3. Give step-by-step advice.\n"
                "4. Use simple farmer-friendly words.\n"
                "5. If not in context, give safe general farming advice."
            )),
            ("human", "{query}")
        ])

        chain = prompt | llm | StrOutputParser()

        try:
            return chain.invoke({
                "context": FARMINGCONTEXT,
                "query": user_query
            })
        except Exception as e:
            return f"❌ Error while generating farming advice: {str(e)}"

    async def _arun(self, user_query: str) -> str:
        raise NotImplementedError("Async not implemented")
    
    
    