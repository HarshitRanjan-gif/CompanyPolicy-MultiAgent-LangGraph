from langchain_core.messages import AIMessage

from state import GraphState


# ==========================================================
# Image Generation Agent
# ==========================================================

def imagegen_agent(state: GraphState) -> GraphState:

    print("\n========== Image Generation Agent ==========")

    answer = (
        "Image generation is not implemented yet."
    )

    state["answer"] = answer

    state["images"] = []

    state["context"] = ""

    state["agent"] = "Image Generation Agent"

    state["messages"].append(
        AIMessage(content=answer)
    )

    return state