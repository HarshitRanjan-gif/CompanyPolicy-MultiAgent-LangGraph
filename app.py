import streamlit as st
import uuid
import time

from chatbot import ask_chatbot
from styles import load_css
from ui import (
    render_sidebar,
    render_header,
    render_user_message,
    render_assistant_message,
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(

    page_title="Company AI Assistant",

    page_icon="🤖",

    layout="wide"

)

load_css()

render_sidebar()

render_header()

# ==========================================================
# SESSION
# ==========================================================

if "messages" not in st.session_state:

    st.session_state.messages = []

if "session_id" not in st.session_state:

    st.session_state.session_id = str(uuid.uuid4())

# ==========================================================
# DISPLAY HISTORY
# ==========================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        render_user_message(message["content"])

    else:

        render_assistant_message(

            answer=message["answer"],

            agent=message["agent"],

            response_time=message["time"],

            context=message["context"],

            pages=message["pages"]

        )

# ==========================================================
# CHAT INPUT
# ==========================================================

question = st.chat_input("Ask anything...")

if question:

    render_user_message(question)

    st.session_state.messages.append(

        {

            "role": "user",

            "content": question

        }

    )

    with st.spinner("🤖 Thinking..."):

        start = time.time()

        result = ask_chatbot(

            question,

            st.session_state.session_id

        )

        end = time.time()

    elapsed = round(end - start, 2)

    render_assistant_message(

        answer=result["answer"],

        agent=result["agent"],

        response_time=elapsed,

        context=result["context"],

        pages=result["pages"]

    )

    st.session_state.messages.append(

        {

            "role": "assistant",

            "answer": result["answer"],

            "agent": result["agent"],

            "time": elapsed,

            "context": result["context"],

            "pages": result["pages"]

        }

    )