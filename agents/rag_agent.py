import os

from dotenv import load_dotenv

from utils.query_rewriter import rewrite_question

from langchain_core.messages import AIMessage
from langchain_groq import ChatGroq

from rag.retriever import get_retriever
from prompts import RAG_PROMPT
from state import GraphState


# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()


# ==========================================================
# LLM
# ==========================================================

llm = ChatGroq(

    groq_api_key=os.getenv("GROQ_API_KEY"),

    model_name="llama-3.1-8b-instant",

    temperature=0.2

)


# ==========================================================
# Retriever
# ==========================================================

retriever = get_retriever()


# ==========================================================
# RAG Agent
# ==========================================================

def rag_agent(state: GraphState) -> GraphState:

    print("\n========== RAG Agent ==========")

    question = state["messages"][-1].content

    print(f"Question : {question}")

    # -----------------------------------------
    # Retrieve Documents
    # -----------------------------------------

    standalone_question = rewrite_question(state)
    documents = retriever.invoke(standalone_question)

    print(f"Retrieved Documents : {len(documents)}")

    pages = []

    context = ""

    for doc in documents:

        page = doc.metadata.get("page")

        if page is not None:

            pages.append(page + 1)

        context += doc.page_content + "\n\n"

    pages = sorted(set(pages))

    # -----------------------------------------
    # No Relevant Documents
    # -----------------------------------------

    if not documents:

        answer = (
            "I couldn't find any relevant information in the company policy "
            "document to answer your question."
        )

    else:

        response = llm.invoke(

            RAG_PROMPT.format_messages(

                question=standalone_question,

                context=context

            )

        )

        answer = response.content

    # -----------------------------------------
    # Update State
    # -----------------------------------------

    state["documents"] = documents

    state["context"] = context

    state["pages"] = pages

    state["answer"] = answer

    state["agent"] = "RAG Agent"

    # Append the assistant message instead of replacing history
    state["messages"].append(

        AIMessage(content=answer)

    )

    return state