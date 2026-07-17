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

    state["standalone_question"] = rewrite_question(state)

    print(f"Latest Question     : {question}")
    print(f"Standalone Question : {state['standalone_question']}")

    question_lower = state["standalone_question"].lower()

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

    imagegen_keywords = [

    "generate an image",

    "generate image",

    "create an image",

    "create image",

    "draw a",

    "draw an",

    "illustrate",

    "render",

    "design a logo",

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

    if contains_keyword(question_lower, imagegen_keywords):

        print("Rule-Based Route : imagegen")

        state["route"] = "imagegen"

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

        "imagegen",

        "llm",

    }

    if route not in valid_routes:

        print(f"⚠ Invalid route: {route}")

        route = "llm"

    print(f"LLM Selected Route : {route}")

    state["route"] = route

    return state