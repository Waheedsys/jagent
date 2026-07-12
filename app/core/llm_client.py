import logging
from langchain_openai import ChatOpenAI
from app.config import settings

logger = logging.getLogger("gateway.agent")

def get_llm_client(model_name: str):
    api_key = settings.openrouter_api_key
    m = model_name if model_name else "openrouter/free"
    return ChatOpenAI(
            model=m,
            openai_api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            temperature=0.7,
            default_headers={
                "HTTP-Referer": "http://localhost:8080",
                "X-Title": "AI Gateway Agent"
            }
    )

async def call_llm(prompt: str, model_name: str | None = None) -> str:
    """Actually invokes the LLM and returns the text response."""
    client = get_llm_client(model_name)
    response = await client.ainvoke(prompt)
    return response.content
