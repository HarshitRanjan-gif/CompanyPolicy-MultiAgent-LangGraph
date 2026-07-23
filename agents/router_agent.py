import re

from dotenv import load_dotenv

from config import get_llm
from prompts import ROUTER_PROMPT
from state import GraphState
from utils.query_rewriter import rewrite_question

load_dotenv()

llm = get_llm(temperature=0)


# ==========================================================
# Helper
# ==========================================================

def contains_keyword(text: str, keywords: list) -> bool:

    for keyword in keywords:

        pattern = r"\b" + re.escape(keyword) + r"\b"

        if re.search(pattern, text):

            return True

    return False


# ==========================================================
# Router
# ==========================================================

def router_agent(state: GraphState) -> GraphState:

    print("\n========== Router Agent ==========")

    question = state["messages"][-1].content

    question_raw_lower = question.lower().strip()

    # -----------------------------------------
    # Identity questions - checked FIRST, before rewriting,
    # so conversation history can never distort these
    # -----------------------------------------

    identity_phrases = [
        "your name",
        "what is your name",
        "who are you",
        "tell me about yourself",
        "introduce yourself",
        "what are you",
        "about yourself",
    ]

    if contains_keyword(question_raw_lower, identity_phrases):

        print("Rule-Based Route : llm (identity)")

        state["standalone_question"] = question  # no rewriting needed

        state["route"] = "llm"

        return state

    state["standalone_question"] = rewrite_question(state)

    print(f"Latest Question     : {question}")
    print(f"Standalone Question : {state['standalone_question']}")

    question_lower = state["standalone_question"].lower()
    raw_question_lower = question.lower()

    # ======================================================
    # RAG
    # ======================================================

    rag_keywords = [

        "leave",
        "attendance",
        "payroll",
        "holiday",
        "employee",
        "policy",
        "policies",
        "office rule",
        "office rules",
        "handbook",
        "benefits",
        "company policy",
        "hr",

    ]

    # ======================================================
    # IMAGE SEARCH
    # ======================================================

    image_keywords = [

    "picture of",
    "pictures of",
    "image of",
    "images of",
    "photo of",
    "photos of",
    "photograph of",
    "pic of",

    "show me a picture",
    "show me an image",
    "show me a photo",

    "give me a picture",
    "give me an image",

    "find a picture",

    ]

    # ======================================================
    # VISION 
    # ======================================================

    vision_keywords = [

    "this image",
    "the image",
    "this picture",
    "the picture",
    "photo",
    "uploaded image",
    "uploaded picture",

    "describe",
    "identify",
    "what is in",
    "who is in",
    "what's in",

    "count",
    "read",
    "extract",
    "ocr",

]
    
    # ======================================================
    # IMAGE GENERATION
    # ======================================================

    # Image Generation
    image_gen_keywords = [
        "generate an image",
        "generate a picture",
        "generate art",
        "create an image",
        "create a picture",
        "draw a picture",
        "draw an image",
        "make an image",
        "make a picture",
        "imagine an image",
        "design an image",
        "generate a",       # catches "generate a dragon", "generate a robot"
        "generate an",
        "create a",
        "create an",
    ]

    # ======================================================
    # WEB SEARCH
    # ======================================================

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

    # ======================================================
    # Rule Based Routing
    # ======================================================
    if (
    state.get("uploaded_image")
    and contains_keyword(question_lower, vision_keywords)
    ):

        print("Rule-Based Route : vision")

        state["route"] = "vision"

        return state
    

    if contains_keyword(question_lower, rag_keywords):

        print("Rule-Based Route : rag")

        state["route"] = "rag"

        return state


    continuation_phrases = ["more", "another", "few more", "again", "one more"]

    word_count = len(raw_question_lower.split())

    is_continuation = (

        word_count <= 4

        and any(phrase in raw_question_lower for phrase in continuation_phrases)

    )

    if is_continuation and state.get("last_image_agent"):

        print(f"Rule-Based Route : {state['last_image_agent']} (continuation)")

        state["route"] = state["last_image_agent"]

        return state

    if contains_keyword(raw_question_lower, image_gen_keywords):

        print("Rule-Based Route : image_gen")

        state["route"] = "image_gen"

        return state

    if contains_keyword(question_lower, image_keywords):

        print("Rule-Based Route : image")

        state["route"] = "image"

        return state

    if contains_keyword(question_lower, web_keywords):

        print("Rule-Based Route : web")

        state["route"] = "web"

        return state

    # ======================================================
    # Ask Router LLM
    # ======================================================

    response = llm.invoke(

        ROUTER_PROMPT.format_messages(

            question=state["standalone_question"]

        )

    )

    route = response.content.strip().lower()

    route = re.sub(r"[^a-z]", "", route)

    valid_routes = {

        "rag",

        "web",

        "image",

        "vision",

        "image_gen",

        "llm",

    }

    if route not in valid_routes:

        print(f"⚠ Invalid route: {route}")

        route = "llm"

    print(f"LLM Selected Route : {route}")

    state["route"] = route

    return state