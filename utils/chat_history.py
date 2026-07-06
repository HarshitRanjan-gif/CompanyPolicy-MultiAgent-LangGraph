# ==========================================================
# Chat History Utility
# ==========================================================

from langchain_core.messages import HumanMessage, AIMessage


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