from memory import memory
from langgraph.graph import StateGraph, START, END

from state import GraphState

from agents.formatter_agent import formatter_agent

from agents.router_agent import router_agent
from agents.rag_agent import rag_agent
from agents.llm_agent import llm_agent
from agents.web_agent import web_agent


# ==========================================================
# Router Logic
# ==========================================================

def route_question(state: GraphState):

    return state["route"]


# ==========================================================
# Build Graph
# ==========================================================

builder = StateGraph(GraphState)


# ==========================================================
# Add Nodes
# ==========================================================

builder.add_node("formatter", formatter_agent)

builder.add_node("router", router_agent)

builder.add_node("rag", rag_agent)

builder.add_node("llm", llm_agent)

builder.add_node("web", web_agent)


# ==========================================================
# Start Edge
# ==========================================================

builder.add_edge(START, "router")


# ==========================================================
# Conditional Routing
# ==========================================================

builder.add_conditional_edges(

    "router",

    route_question,

    {

        "rag": "rag",

        "llm": "llm",

        "web": "web"

    }

)


# ==========================================================
# End Edges
# ==========================================================

builder.add_edge("rag", "formatter")

builder.add_edge("llm", "formatter")

builder.add_edge("web", "formatter")

builder.add_edge("formatter", END)


# ==========================================================
# Compile Graph
# ==========================================================

graph = builder.compile(

    checkpointer=memory

)