import uuid

from langchain_core.messages import HumanMessage

from graph import graph


def ask_chatbot(question, session_id=None, uploaded_image=None, uploaded_image_type=None):

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

            "images": [],

            "uploaded_image": uploaded_image or "",

            "uploaded_image_type": uploaded_image_type or "",

            "generated_images": [],

            "answer": ""

        },

        config={

            "configurable": {

                "thread_id": session_id

            }

        }

    )

    return result


def ask_chatbot_stream(question, session_id=None, uploaded_image=None, uploaded_image_type=None):

    if session_id is None:

        session_id = str(uuid.uuid4())

    initial_state = {

        "messages": [HumanMessage(content=question)],

        "standalone_question": "",

        "route": "",

        "agent": "",

        "documents": [],

        "context": "",

        "pages": [],

        "images": [],

        "uploaded_image": uploaded_image or "",

        "uploaded_image_type": uploaded_image_type or "",

        "generated_images": [],

        "answer": ""

    }

    config = {

        "configurable": {

            "thread_id": session_id

        }

    }

    for step in graph.stream(initial_state, config=config, stream_mode="updates"):

        yield step