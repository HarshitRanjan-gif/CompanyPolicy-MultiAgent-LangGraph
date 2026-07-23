import re
import time

from langchain_core.messages import AIMessage

from config import get_llm

from utils.query_rewriter import rewrite_question

from tools.image_gen import generate_image

from state import GraphState


# ==========================================================
# LLM (for real-person safety check)
# ==========================================================

llm = get_llm(temperature=0)


# ==========================================================
# Subject Extraction
# ==========================================================

STRIP_WORDS = [

    "can you", "could you", "please", "i want", "i need",

    "generate", "create", "draw", "make", "design", "imagine",
    "give", "show", "find",

    "me",

    "a few", "few", "more", "additional", "another", "some",

    "an", "a",

    "images", "image", "pictures", "picture", "photos", "photo",
    "pics", "pic", "illustrations", "illustration",
    "artworks", "artwork", "art",

    "of", "showing", "depicting", "with",

]


def extract_generation_subject(question: str) -> str:

    q = question.lower().strip()

    q = re.sub(r"^\d+\s+", "", q)

    changed = True

    while changed:

        changed = False

        for word in STRIP_WORDS:

            if q.startswith(word + " "):

                q = q[len(word):].strip()

                changed = True

                break

            elif q == word:

                q = ""

                changed = True

                break

    q = q.rstrip("?.! ").strip()

    return q if q else question

# ==========================================================
# Real Person Safety Check
# ==========================================================

def is_real_person_request(subject: str) -> bool:

    prompt = f"""Does the following image request refer to a specific real, named individual
(celebrity, politician, historical figure, athlete, or any real named person)?

Answer with ONLY one word: yes or no.

Request: {subject}
"""

    try:

        response = llm.invoke(prompt)

        return "yes" in response.content.strip().lower()

    except Exception:

        return False


# ==========================================================
# Image Generation Agent
# ==========================================================

def image_gen_agent(state: GraphState) -> GraphState:

    print("\n========== Image Generation Agent ==========")

    if not state.get("standalone_question"):

        state["standalone_question"] = rewrite_question(state)

    standalone_question = state["standalone_question"]

    subject = extract_generation_subject(standalone_question)

    print(f"Generation Subject : {subject}")

    # -----------------------------------------
    # Safety Check - Real Named People
    # -----------------------------------------

    if is_real_person_request(subject):

        answer = (
            "I can't generate images of real, named people. "
            "If you'd like a photo of someone specific, try asking me to "
            "**find a picture of them** instead. I'm happy to generate "
            "images of fictional characters, objects, or scenes though!"
        )

        state["generated_images"] = []

        state["answer"] = answer

        state["agent"] = "Image Generation Agent"

        state["messages"].append(

            AIMessage(content=answer)

        )

        state["last_image_agent"] = "image_gen"

        return state

    # -----------------------------------------
    # Generate Image (always 1 per request)
    # -----------------------------------------

    image_url = generate_image(subject)

    answer = f"Here's what I created for **{subject}**:"

    state["generated_images"] = [image_url]

    state["answer"] = answer

    state["agent"] = "Image Generation Agent"

    state["messages"].append(

        AIMessage(content=answer)

    )

    state["last_image_agent"] = "image_gen"

    return state