from dotenv import load_dotenv

from langchain_core.messages import AIMessage

from state import GraphState

from utils.query_rewriter import rewrite_question

from tools.image_analysis import analyze_image

load_dotenv()


# ==========================================================
# Vision Agent
# ==========================================================

def vision_agent(state: GraphState) -> GraphState:

    print("\n========== Vision Agent ==========")

    question = state["messages"][-1].content

    standalone_question = state["standalone_question"]

    image_path = state.get("uploaded_image")

    print(f"Uploaded Image: {image_path}")

    if not image_path:

        answer = "No image was uploaded."

    else:

        answer = analyze_image(

            image_path=image_path,

            question=standalone_question,

        )

    state["image_analysis"] = answer

    state["answer"] = answer

    state["agent"] = "Vision Agent"

    state["vision_model"] = "Gemini 3.5 Flash"

    state["messages"].append(

        AIMessage(content=answer)

    )

    return state