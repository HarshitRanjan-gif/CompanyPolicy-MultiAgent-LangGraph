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

    # -----------------------------------------
    # Ensure Generated Images Exist
    # -----------------------------------------

    if "generated_images" not in state or state["generated_images"] is None:
        state["generated_images"] = []

    # -----------------------------------------
    # Ensure Images Exist
    # -----------------------------------------

    if "images" not in state or state["images"] is None:
        state["images"] = []

    print("Response formatted successfully.")

    return state