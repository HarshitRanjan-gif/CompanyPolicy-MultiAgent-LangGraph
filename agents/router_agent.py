import os
import re

from dotenv import load_dotenv

from langchain_groq import ChatGroq

from utils.query_rewriter import rewrite_question

from prompts import ROUTER_PROMPT

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

    temperature=0

)


# ==========================================================
# Router Agent
# ==========================================================

def router_agent(state: GraphState) -> GraphState:

    print("\n========== Router Agent ==========")

    # -----------------------------------------
    # Rewrite Question
    # -----------------------------------------

    question = state["messages"][-1].content

    state["standalone_question"] = rewrite_question(state)

    print(f"Latest Question     : {question}")
    print(f"Standalone Question : {state['standalone_question']}")

    question_lower = state["standalone_question"].lower()

    # -----------------------------------------
    # Rule-Based Routing
    # -----------------------------------------

    # Company Policy (RAG)
    rag_keywords = [
        "leave",
        "attendance",
        "payroll",
        "holiday",
        "hr",
        "employee",
        "policy",
        "policies",
        "office rule",
        "office rules",
        "handbook",
        "benefits",
        "company policy",
    ]

    # Current / External Information (WEB)
    web_keywords = [
        "current",
        "today",
        "latest",
        "recent",
        "news",
        "weather",
        "temperature",
        "forecast",
        "stock",
        "stock price",
        "share price",
        "ceo",
        "founder",
        "president",
        "prime minister",
        "governor",
        "minister",
        "election",
        "live",
        "breaking",
        "released",
        "release date",
        "version",
        "price",
        "cost",
        "fees",
        "salary",
        "private limited",
        "pvt ltd",
        "limited",
        "inc",
        "llp",
        "corporation",
    ]

    # ---------- RAG ----------

    if any(keyword in question_lower for keyword in rag_keywords):

        print("Rule-Based Route : rag")

        state["route"] = "rag"

        return state

    # ---------- WEB ----------

    if any(keyword in question_lower for keyword in web_keywords):

        print("Rule-Based Route : web")

        state["route"] = "web"

        return state

    # -----------------------------------------
    # Ask Router LLM
    # -----------------------------------------

    response = llm.invoke(

        ROUTER_PROMPT.format_messages(

            question=state["standalone_question"]

        )

    )

    # -----------------------------------------
    # Extract Route
    # -----------------------------------------

    route = response.content.strip().lower()

    route = re.sub(r"[^a-z]", "", route)

    # -----------------------------------------
    # Validate Route
    # -----------------------------------------

    valid_routes = {"rag", "web", "llm"}

    if route not in valid_routes:

        print(f"⚠️ Invalid route received: {route}")

        route = "llm"

    print(f"LLM Selected Route : {route}")

    # -----------------------------------------
    # Update State
    # -----------------------------------------

    state["route"] = route

    return state