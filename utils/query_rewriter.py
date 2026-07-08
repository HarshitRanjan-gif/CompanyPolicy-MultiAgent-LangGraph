import os

from dotenv import load_dotenv

from config import get_llm

from langchain_groq import ChatGroq

from utils.chat_history import get_conversation, get_recent_messages


# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()


# ==========================================================
# LLM
# ==========================================================

llm = get_llm(temperature=0)


# ==========================================================
# Rewrite Question
# ==========================================================

def rewrite_question(state):

    question = state["messages"][-1].content

    recent_messages = get_recent_messages(state["messages"])

    conversation = get_conversation(recent_messages)

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