import os
import re

from dotenv import load_dotenv

from langchain_core.messages import AIMessage

from config import get_llm

from utils.query_rewriter import rewrite_question

from langchain_groq import ChatGroq

from tools.search import web_search, image_search

from state import GraphState


# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()


# ==========================================================
# LLM
# ==========================================================

llm = get_llm()


# ==========================================================
# Image Request Keywords
# ==========================================================

IMAGE_KEYWORDS = [
    "picture of",
    "image of",
    "photo of",
    "photograph of",
    "show me a picture",
    "show me an image",
    "show me a photo",
    "give a picture",
    "give an image",
    "give a photo",
    "pic of",
]


def is_image_request(question: str) -> bool:

    question_lower = question.lower()

    return any(keyword in question_lower for keyword in IMAGE_KEYWORDS)


import re

def extract_image_subject(question: str) -> str:

    q = question.lower().strip()

    patterns = [

        r".*?(?:picture|image|photo|photograph|pic)\s+of\s+",

        r".*?show\s+me\s+(?:a\s+)?(?:picture|image|photo|pic)\s+of\s+",

        r".*?give\s+me\s+(?:a\s+)?(?:picture|image|photo|pic)\s+of\s+",

        r".*?find\s+(?:a\s+)?(?:picture|image|photo|pic)\s+of\s+",

        r".*?where\s+can\s+i\s+find\s+(?:a\s+)?(?:picture|image|photo|pic)\s+of\s+",

    ]

    for pattern in patterns:

        q = re.sub(pattern, "", q)

    return q.strip(" ?.!")

# ==========================================================
# Web Agent
# ==========================================================

def web_agent(state: GraphState) -> GraphState:

    print("\n========== Web Agent ==========")

    question = state["messages"][-1].content

    print(f"Question : {question}")

    standalone_question = rewrite_question(state)

    # -----------------------------------------
    # Image Request Path
    # -----------------------------------------

    if is_image_request(standalone_question):

        image_subject = extract_image_subject(standalone_question)

        print(f"Image Subject Extracted : {image_subject}")

        images = image_search(image_subject)

        if images:

            answer = "Here are some images I found:"

        else:

            answer = "I couldn't find any images for that."

        state["images"] = images

        state["context"] = ""

        state["answer"] = answer

        state["agent"] = "Web Search Agent"

        state["messages"].append(

            AIMessage(content=answer)

        )

        return state

    # -----------------------------------------
    # Normal Text Search Path
    # -----------------------------------------

    search_result = web_search(standalone_question)

    context = ""

    for result in search_result["results"]:

        context += f"Title: {result['title']}\n"

        context += f"Content: {result['content']}\n\n"

    prompt = f"""
You are a professional AI assistant.

The user's question has already been rewritten into a standalone question.

Question:

{standalone_question}

Web Search Results:

{context}

Instructions:

1. Answer ONLY the user's question.
2. Ignore any unrelated information in the search results.
3. Do not summarize every search result — combine only the relevant information.
4. If multiple search results exist and they conflict or cover different entities (e.g. different countries, versions, or time periods), clearly separate them instead of blending them together.
5. If the answer cannot be found, say:
"I couldn't find sufficient information."
6. Provide a complete, well-explained answer. Include relevant details such as names, dates, numbers, or context where available, but avoid repeating the same point multiple times.
7. Format your answer using Markdown headers and bullet lists. Use "##" for section headings when the answer has multiple distinct parts, and "-" for bullet points when listing multiple facts or items. Keep paragraphs short and scannable rather than one dense block of text.

Now answer the user's question.
"""

    response = llm.invoke(prompt)


    # -----------------------------------------
    # Update State
    # -----------------------------------------

    state["images"] = []

    state["context"] = context

    state["answer"] = response.content

    state["agent"] = "Web Search Agent"

    state["messages"].append(

        AIMessage(content=response.content)

    )

    return state