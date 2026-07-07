import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# ==========================================================
# LLM Load
# ==========================================================

def get_llm(temperature: float = 0.2, max_tokens: int = 1024):
    return ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.3-70b-versatile",
        temperature=temperature,
        max_tokens=max_tokens,
    )