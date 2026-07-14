from typing import TypedDict, List, Annotated, Optional

from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class GraphState(TypedDict):
    """
    Shared state passed between all LangGraph nodes.
    """

    # ==========================================================
    # Conversation
    # ==========================================================

    messages: Annotated[list[BaseMessage], add_messages]

    standalone_question: str

    # ==========================================================
    # Routing
    # ==========================================================

    route: str

    agent: str

    # ==========================================================
    # RAG
    # ==========================================================

    documents: List[Document]

    pages: List[int]

    context: str

    # ==========================================================
    # Image Search
    # ==========================================================

    images: List[str]

    image_count: int

    shown_images: dict[str, set[str]]

    # ==========================================================
    # Uploaded Image
    # ==========================================================

    uploaded_image: Optional[str]

    # ==========================================================
    # Image Analysis
    # ==========================================================

    image_analysis: str

    # ==========================================================
    # Image Generation
    # ==========================================================

    generated_images: List[str]

    # ==========================================================
    # Final Response
    # ==========================================================

    answer: str