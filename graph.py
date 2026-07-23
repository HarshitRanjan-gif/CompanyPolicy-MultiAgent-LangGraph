from memory import memory
from langgraph.graph import StateGraph, START, END

from state import GraphState

from agents.formatter_agent import formatter_agent
from agents.router_agent import router_agent

from agents.rag_agent import rag_agent
from agents.web_agent import web_agent
from agents.llm_agent import llm_agent

from agents.image_agent import image_agent
from agents.vision_agent import vision_agent
from agents.image_gen_agent import image_gen_agent


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

builder.add_node("router", router_agent)

builder.add_node("rag", rag_agent)

builder.add_node("web", web_agent)

builder.add_node("image", image_agent)

builder.add_node("vision", vision_agent)

builder.add_node("image_gen", image_gen_agent)

builder.add_node("llm", llm_agent)

builder.add_node("formatter", formatter_agent)


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

        "web": "web",

        "image": "image",

        "vision": "vision",

        "image_gen": "image_gen",

        "llm": "llm",

    }

)


# ==========================================================
# End Edges
# ==========================================================

builder.add_edge("rag", "formatter")

builder.add_edge("web", "formatter")

builder.add_edge("image", "formatter")

builder.add_edge("vision", "formatter")

builder.add_edge("image_gen", "formatter")

builder.add_edge("llm", "formatter")

builder.add_edge("formatter", END)


# ==========================================================
# Compile Graph
# ==========================================================

graph = builder.compile(

    checkpointer=memory

)