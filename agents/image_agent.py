import re

from dotenv import load_dotenv

from langchain_core.messages import AIMessage

from state import GraphState

from utils.query_rewriter import rewrite_question

from tools.image_search import (image_search,parse_request,)

from tools.image_analysis import analyze_image


# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()

# ==========================================================
# Image Agent
# ==========================================================

def image_agent(state: GraphState) -> GraphState:

    print("\n========== Image Agent ==========")

    question = state["messages"][-1].content

    standalone_question = rewrite_question(state)

    print(f"Question : {question}")

    print(f"Standalone : {standalone_question}")

    # ======================================================
    # Image Search
    # ======================================================

    print("Mode : Image Search")

    # -----------------------------------------
    # Parse request
    # -----------------------------------------

    request = parse_request(standalone_question)

    query = request["query"].strip().lower()

    print(f"Query : {query}")

    # -----------------------------------------
    # Restore image history
    # -----------------------------------------

    shown_images = state.get("shown_images")

    if shown_images is None:
        shown_images = {}

    print("\n========== Image History ==========")
    print(shown_images)

    # -----------------------------------------
    # Previously shown URLs
    # -----------------------------------------

    exclude_urls = set(
        shown_images.get(query, [])
    )

    print(f"\nPrevious images shown: {len(exclude_urls)}")

    for i, url in enumerate(exclude_urls, 1):
        print(f"{i}. {url}")

    # -----------------------------------------
    # Search
    # -----------------------------------------

    result = image_search(
        standalone_question,
        exclude_urls=exclude_urls,
    )

    images = result["images"]

    image_count = len(images)

    # -----------------------------------------
    # Build answer
    # -----------------------------------------

    if images:

        answer = (
            f"Here {'is' if image_count == 1 else 'are'} "
            f"{image_count} image{'s' if image_count != 1 else ''} I found."
        )

    else:

        answer = "I couldn't find any images."

    state["images"] = images

    # -----------------------------------------
    # Update image history
    # -----------------------------------------

    shown_images.setdefault(query, [])

    shown_images[query].extend(images)

    # Remove duplicate URLs while preserving order
    shown_images[query] = list(
        dict.fromkeys(shown_images[query])
    )

    print(f"\nTotal remembered images: {len(shown_images[query])}")

    state["shown_images"] = shown_images

    print("\n========== Updated Image History ==========")
    print(state["shown_images"])

    # -----------------------------------------
    # Update state
    # -----------------------------------------

    state["answer"] = answer

    state["context"] = ""

    state["agent"] = "Image Agent"

    state["messages"].append(
        AIMessage(content=answer)
    )

    return state