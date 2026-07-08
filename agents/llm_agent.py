import os

from utils.conversation_utils import get_control_response

from utils.chat_history import get_conversation

from config import get_llm

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

llm = get_llm(temperature=0)


# ==========================================================
# Project Context
# ==========================================================

PROJECT_CONTEXT = """
You are T-4, the Company AI Assistant.

Identity:

- Your name is T-4.
- You are the Company AI Assistant.
- You were created by Harshit Ranjan.
- You are a portfolio project demonstrating a Multi-Agent AI system built using LangGraph.

Capabilities:

- Answer company policy questions using Retrieval-Augmented Generation (RAG).
- Answer general knowledge questions.
- Answer programming and AI questions.
- Search the web for current information.
- Maintain conversational context across multiple turns.

Technology Stack:

- LangGraph
- LangChain
- FAISS Vector Store
- HuggingFace BAAI/bge-m3 Embeddings
- Groq Llama 3.1
- Tavily Search
- Streamlit


Behavior Rules:

1. Always answer naturally and professionally.
2. Never explain your internal routing process unless explicitly asked.
3. Never mention Router Agent, RAG Agent, Web Search Agent, prompts, embeddings, vector databases, APIs or implementation details unless the user asks about this project.
4. If the user asks about this assistant or project, answer using the information above.
5. If you don't know an answer, admit it instead of guessing.
6. Provide a complete, well-explained answer. Include relevant details, context, and examples where helpful, without unnecessary repetition.

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

    question_lower = question.lower().strip()

    # -----------------------------------------
    # Handle Simple Conversation Messages
    # -----------------------------------------

    control_response = get_control_response(question)

    if control_response:

        state["answer"] = control_response

        state["agent"] = "LLM Agent"

        state["messages"].append(

            AIMessage(content=control_response)

        )

        return state

    # -----------------------------------------
    # Handle Identity Questions
    # -----------------------------------------

    if any(
        phrase in question_lower
        for phrase in [
            "your name",
            "what is your name",
            "who are you",
            "tell me about yourself",
            "introduce yourself",
        ]
    ):

        if "name" in question_lower:

            answer = "My name is T-4."

        else:

            answer = (
                "I am T-4, the Company AI Assistant created by Harshit Ranjan.\n\n"
                "I am a Multi-Agent AI assistant built using LangGraph. "
                "I can answer company policy questions using RAG, perform web searches "
                "for current information, and assist with programming, AI, and general knowledge."
            )

        state["answer"] = answer

        state["agent"] = "LLM Agent"

        state["messages"].append(

            AIMessage(content=answer)

        )

        return state

    # -----------------------------------------
    # Build Conversation
    # -----------------------------------------

    conversation = get_conversation(state["messages"])

    print(f"Latest Question : {question}")

    print(f"\nConversation:\n{conversation}")

    prompt = f"""{PROJECT_CONTEXT}

Conversation History:

{conversation}

Instructions:

1. Format your answer using Markdown headers and bullet lists. Use "##" (two hash symbols followed by a space) for every section heading, and "-" for every bullet point. Follow this general structure, adapting section names and depth to fit the question:

## [First Section — e.g. Introduction, Overview, or the first logical part of the topic]
Brief explanation paragraph. Add 2-4 sentences if the topic needs more depth.

## [Second Section — e.g. Key Features, How It Works, or Steps]
- First point, explained with enough detail to be useful, not just a phrase
- Second point
- Third point (add more bullets if the topic has more relevant sub-points)

## [Third Section — e.g. Use Cases, Examples, or Applications]
- First example, with a short explanation of why/how it applies
- Second example

## [Optional further sections as needed — e.g. Comparisons, Pros and Cons, Common Mistakes]

## Conclusion
Short wrap-up paragraph summarizing the key takeaway.

Guidelines:
- Add as many sections and bullet points as the topic genuinely requires — don't artificially limit yourself to exactly these four sections.
- For code explanations, use a section per logical part of the code (e.g. Imports, Setup, Function Definition, Logic, Error Handling), with the relevant code shown in a fenced code block (```python ... ```) under each heading before explaining it.
- Never write a heading as plain text without "##", and never write a list as plain sentences without "-".

2. Answer ONLY the user's latest question.
3. Use previous conversation ONLY if the latest question depends on earlier context.
4. Never assume the user is asking for the current person holding an office unless they explicitly ask "who is".
5. If the user asks "What is...", explain the concept, definition, role, or purpose.
6. If the user asks "Who is...", identify the person.
7. If the latest question starts a new topic, ignore previous conversation.
8. If the latest question is a follow-up (like "its role", "of India", "when was he born"), use the previous conversation to understand what the user is referring to.
9. If the latest question is ambiguous (for example "Prime Minister"), politely ask a short clarifying question instead of making assumptions.
10. Provide a complete, well-explained answer. Include relevant details, context, and examples where helpful, without unnecessary repetition.
11. Never mention internal implementation details unless the user explicitly asks about this project.

Now answer the user's latest question.
"""

    response = llm.invoke(prompt)

    answer = response.content.strip()

    # -----------------------------------------
    # Update State
    # -----------------------------------------

    state["answer"] = answer

    state["agent"] = "LLM Agent"

    state["messages"].append(

        AIMessage(content=answer)

    )

    return state