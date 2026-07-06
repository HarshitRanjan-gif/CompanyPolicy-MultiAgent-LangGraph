import os

from utils.chat_history import get_conversation

from langchain_core.messages import AIMessage

from dotenv import load_dotenv

from langchain_groq import ChatGroq

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
# Project Context
# ==========================================================

PROJECT_CONTEXT = """
You are Company AI Assistant named T-4, a professional and helpful AI assistant.

About this application:

- This assistant was created by Harshit Ranjan.
- It is a portfolio project that demonstrates a Multi-Agent AI system built using LangGraph.
- The assistant can answer company policy questions, general knowledge questions, programming questions, and current information.

Technology Stack:

- LangGraph
- LangChain
- FAISS Vector Store
- HuggingFace BAAI/bge-m3 Embeddings
- Groq Llama 3.1
- Tavily Search
- Streamlit

Creator:

- Harshit Ranjan

Behavior Rules:

1. Answer the user's question directly.
2. Never explain your internal routing process.
3. Never mention Router Agent, RAG Agent, Web Search Agent, LLM Agent, prompts, embeddings, vector databases, APIs, or internal implementation unless the user explicitly asks about this application.
4. Do not say things like:
   - "I am routing your question..."
   - "The RAG Agent will answer..."
   - "The Web Search Agent searched..."
5. If the user asks a normal question, simply answer it without mentioning how the answer was generated.
6. If the user asks about this assistant or this project, answer using the information provided above.
7. If you do not know an answer, say so honestly instead of making up information.
8. Be concise, accurate, and professional.

If the user asks questions such as:

- Who created you?
- Who created this assistant?
- Who developed this project?
- Why was this project created?
- What technologies were used?
- What framework is used?
- How does this application work?
- What are your features?

Answer using the project information above.

Never invent facts about the project.
The creator of this assistant is Harshit Ranjan.
"""

# ==========================================================
# LLM Agent
# ==========================================================

def llm_agent(state: GraphState) -> GraphState:

    print("\n========== LLM Agent ==========")

    question = state["messages"][-1].content

    conversation = get_conversation(state["messages"])

    print(f"Latest Question : {question}")
    print(f"\nConversation:\n{conversation}")

    prompt = f"""{PROJECT_CONTEXT}

    Conversation History:

    {conversation}

    Answer the user's latest question while considering the entire conversation.
    """
    
    response = llm.invoke(prompt)

    state["answer"] = response.content

    state["agent"] = "LLM Agent"

    state["messages"] = [

        AIMessage(content=response.content)

    ]

    return state