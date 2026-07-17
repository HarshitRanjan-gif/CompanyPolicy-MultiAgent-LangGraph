import re
import os

from dotenv import load_dotenv
from config import get_llm

from utils.chat_history import (
    get_conversation,
    get_recent_messages,
)

load_dotenv()

llm = get_llm(temperature=0)


# ==========================================================
# Small Talk
# ==========================================================

SMALL_TALK = {
    "hi",
    "hello",
    "hey",
    "thanks",
    "thank you",
    "thankyou",
    "ok",
    "okay",
    "ok thanks",
    "okay thanks",
    "ok done",
    "ok done thanks",
    "done",
    "bye",
    "goodbye",
    "good night",
    "good morning",
    "good afternoon",
    "good evening",
    "see you",
    "nice",
    "great",
    "awesome",
    "cool",
}


# ==========================================================
# Rewrite Question
# ==========================================================

def rewrite_question(state):

    question = state["messages"][-1].content.strip()

    question_lower = re.sub(r"\s+", " ", question.lower())

    # -----------------------------------------
    # Skip rewriting for greetings / small talk
    # -----------------------------------------

    if question_lower in SMALL_TALK:

        print("\n========== Query Rewriter ==========")
        print(f"Original : {question}")
        print("Rewritten : (Skipped)")
        print()

        return question

    recent_messages = get_recent_messages(state["messages"])

    conversation = get_conversation(recent_messages)

    prompt = f"""
You are a query rewriting assistant.

Rewrite ONLY when needed.

Rules:

- Preserve the user's meaning exactly.
- Never change facts.
- Never guess what the user intended.
- Never replace named entities.
- Never rewrite greetings, thanks, confirmations or acknowledgements.
- If the question is already complete, return it unchanged.

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