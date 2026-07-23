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

Your job is to rewrite the user's latest message into a complete, standalone
question by filling in any missing subject, topic, or context using the
conversation history - NOT by inventing new facts.

Rules:

- If the latest message refers back to something discussed earlier (e.g. "5 more",
  "another one", "what about her", "the same thing"), rewrite it to explicitly
  include that subject/topic from the conversation history.
- Do not invent details, facts, or subjects that are not present anywhere in the
  conversation history.
- Do not change or reinterpret named entities - use them exactly as they appeared.
- If the question is already complete and self-contained, return it unchanged.
- Never rewrite greetings, thanks, confirmations or acknowledgements.
- Output ONLY the rewritten question itself. Do NOT explain your reasoning,
  do NOT add labels like "Standalone Question:", do NOT add any commentary
  before or after the question.

Examples (showing INPUT -> OUTPUT only, exactly what you should return):

Conversation: User asked for "2 images of Taylor Swift"
Latest Message: "5 more images"
Output: 5 more images of Taylor Swift

Conversation: User asked to "generate a picture of a sunset"
Latest Message: "make it more colorful"
Output: generate a more colorful picture of a sunset

Conversation:

{conversation}

Latest Question:

{question}

Output:
"""

    response = llm.invoke(prompt)

    rewritten_question = response.content.strip()

    # -----------------------------------------
    # Defensive cleanup - strip any leaked reasoning/preamble
    # -----------------------------------------

    rewritten_question = rewritten_question.split("\n")[0].strip()

    for prefix in [
        "the standalone question is:",
        "standalone question:",
        "output:",
        "rewritten question:",
    ]:

        if rewritten_question.lower().startswith(prefix):

            rewritten_question = rewritten_question[len(prefix):].strip()

    print("\n========== Query Rewriter ==========")
    print(f"Original : {question}")
    print(f"Rewritten : {rewritten_question}")

    return rewritten_question