from state import GraphState


# ==========================================================
# Formatter Agent
# ==========================================================

def formatter_agent(state: GraphState) -> GraphState:

    print("\n========== Formatter Agent ==========")

    # -----------------------------------------
    # Clean Answer
    # -----------------------------------------

    answer = state.get("answer", "").strip()

    state["answer"] = answer

    # -----------------------------------------
    # Ensure Context Exists
    # -----------------------------------------

    if "context" not in state or state["context"] is None:
        state["context"] = ""

    # -----------------------------------------
    # Ensure Documents Exist
    # -----------------------------------------

    if "documents" not in state or state["documents"] is None:
        state["documents"] = []

    print("Response formatted successfully.")

    return state