import os
from dotenv import load_dotenv
from typing import Type
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.tools import BaseTool

from app.data.goverment_schemas import GOVERMENTSCHEMES

load_dotenv()


# ✅ Input Schema (VERY IMPORTANT for agents)
class GovSchemeInput(BaseModel):
    user_query: str = Field(..., description="User question about Indian government agricultural schemes")


# ✅ Create LLM once (efficient)
def get_llm():
    return ChatOpenAI(
        api_key=os.getenv("SARVAM_MODEL_API"),
        base_url="https://api.sarvam.ai/v1",
        model=os.getenv("SARVAM30_MODEL_NAME"),
        temperature=0.1
    )


# ✅ Tool Class (Best Practice)
class GovSchemeRAGTool(BaseTool):
    name: str = "government_scheme_rag"
    description: str = (
        "Use this tool to answer questions about Indian government agricultural schemes. "
        "It provides details like eligibility, benefits, and application process. "
        "Works in multiple Indian languages."
    )
    args_schema: Type[BaseModel] = GovSchemeInput

    def _run(self, user_query: str) -> str:
        llm = get_llm()

        prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "You are 'Yojana Sahayak', an expert on Indian Government Agricultural Schemes.\n"
                "GOVERNMENT DATA CONTEXT:\n{context}\n\n"
                "INSTRUCTIONS:\n"
                "1. Detect the language of the user's question.\n"
                "2. Answer ONLY using the provided context in the SAME language.\n"
                "3. If info is missing, say you don't have details.\n"
                "4. Focus on Eligibility, Benefits, and How to Apply."
            )),
            ("human", "{query}")
        ])

        chain = prompt | llm | StrOutputParser()

        try:
            return chain.invoke({
                "context": GOVERMENTSCHEMES,
                "query": user_query
            })
        except Exception as e:
            return f"Error while fetching scheme information: {str(e)}"

    async def _arun(self, user_query: str) -> str:
        raise NotImplementedError("Async not implemented")