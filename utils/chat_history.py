# utils/chat_history.py

from langchain_core.messages import HumanMessage, AIMessage


# ==========================================================
# Limit Conversation History
# ==========================================================

def get_recent_messages(messages, limit: int = 20):

    return messages[-limit:]


# ==========================================================
# Chat History Utility
# ==========================================================

def get_conversation(messages):

    conversation = []

    for message in messages:

        if isinstance(message, HumanMessage):

            conversation.append(
                f"User: {message.content}"
            )

        elif isinstance(message, AIMessage):

            conversation.append(
                f"Assistant: {message.content}"
            )

    return "\n".join(conversation)