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

    standalone_question = rewrite_question(state)

    print(f"Latest Question     : {question}")
    print(f"Standalone Question : {standalone_question}")

    # -----------------------------------------
    # Ask Router LLM
    # -----------------------------------------

    response = llm.invoke(

        ROUTER_PROMPT.format_messages(

            question=standalone_question

        )

    )

    # -----------------------------------------
    # Extract Route
    # -----------------------------------------

    route = response.content.strip().lower()

    # Keep only letters (handles llm., web:, rag,)
    route = re.sub(r"[^a-z]", "", route)

    # -----------------------------------------
    # Validate Route
    # -----------------------------------------

    valid_routes = {"rag", "web", "llm"}

    if route not in valid_routes:

        print(f"⚠️ Invalid route received: {route}")

        route = "llm"

    print(f"Selected Route : {route}")

    # -----------------------------------------
    # Update State
    # -----------------------------------------

    state["route"] = route

    state["standalone_question"] = standalone_question

    return state