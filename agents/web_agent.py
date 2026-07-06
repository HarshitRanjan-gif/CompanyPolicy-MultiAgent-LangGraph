import os

from dotenv import load_dotenv

from langchain_core.messages import AIMessage

from utils.query_rewriter import rewrite_question

from langchain_groq import ChatGroq

from tools.search import web_search

from state import GraphState


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

    temperature=0.2

)


# ==========================================================
# Web Agent
# ==========================================================

def web_agent(state: GraphState) -> GraphState:

    print("\n========== Web Agent ==========")

    question = state["messages"][-1].content

    print(f"Question : {question}")


    # -----------------------------------------
    # Search the Web
    # -----------------------------------------

    standalone_question = rewrite_question(state)
    search_result = web_search(standalone_question)


    # -----------------------------------------
    # Build Context
    # -----------------------------------------

    context = ""

    for result in search_result["results"]:

        context += f"Title: {result['title']}\n"

        context += f"Content: {result['content']}\n\n"


    # -----------------------------------------
    # Generate Answer
    # -----------------------------------------

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
3. Do not summarize every search result.
4. If multiple search results exist, combine only the relevant information.
5. If the answer cannot be found, say:
"I couldn't find sufficient information."

Give a concise and accurate answer.
"""


    response = llm.invoke(prompt)


    # -----------------------------------------
    # Update State
    # -----------------------------------------

    state["context"] = context

    state["answer"] = response.content

    state["agent"] = "Web Search Agent"

    state["messages"].append(

        AIMessage(content=response.content)

    )

    return state