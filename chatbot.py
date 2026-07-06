import uuid

from langchain_core.messages import HumanMessage

from graph import graph


def ask_chatbot(question, session_id=None):

    if session_id is None:

        session_id = str(uuid.uuid4())

    result = graph.invoke(

        {

            "messages": [HumanMessage(content=question)],

            "standalone_question": "",

            "route": "",

            "agent": "",

            "documents": [],

            "context": "",

            "pages": [],

            "answer": ""

        },

        config={

            "configurable": {

                "thread_id": session_id

            }

        }

    )

    return result