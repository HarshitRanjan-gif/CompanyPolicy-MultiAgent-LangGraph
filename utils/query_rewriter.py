import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq

from utils.chat_history import get_conversation


# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()


# ==========================================================
# LLM
# ==========================================================

llm = ChatGroq(

    groq_api_key=os.getenv("GROQ_API_KEY"),

    model_name="llama-3.1-8b-instant",

    temperature=0

)


# ==========================================================
# Rewrite Question
# ==========================================================

def rewrite_question(state):

    question = state["messages"][-1].content

    conversation = get_conversation(state["messages"])

    prompt = f"""
You are an AI assistant.

Your task is to rewrite the user's latest question into a complete standalone question.

Use the previous conversation only if it is required.

Rules:

- Do NOT answer the question.
- Do NOT explain.
- Return ONLY the rewritten question.
- If the latest question is already complete, return it unchanged.

Conversation:

{conversation}

Latest Question:

{question}

Standalone Question:
"""

    response = llm.invoke(prompt)

    rewritten_question = response.content.strip()

    print("\n========== Query Rewriter ==========")

    print(f"Original : {question}")

    print(f"Rewritten : {rewritten_question}")

    return rewritten_question