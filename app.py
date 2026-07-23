import streamlit as st
import uuid
import time
import tempfile
import os

from chatbot import ask_chatbot
from chatbot import ask_chatbot_stream
from styles import load_css
from ui import (
    render_sidebar,
    render_header,
    render_user_message,
    render_assistant_message,
    render_chat_input,
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(

    page_title="Smart AI Assistant",

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

if "active_image" not in st.session_state:
    st.session_state.active_image = None

if "active_image_name" not in st.session_state:
    st.session_state.active_image_name = None

if "upload_key" not in st.session_state:
    st.session_state.upload_key = 0

if "last_uploaded_file_id" not in st.session_state:
    st.session_state.last_uploaded_file_id = None    
# ==========================================================
# DISPLAY HISTORY
# ==========================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        render_user_message(

            message["content"],

            image_path=message.get("uploaded_image"),

        )

    else:

        render_assistant_message(

            answer=message["answer"],

            agent=message["agent"],

            response_time=message["time"],

            context=message["context"],

            pages=message["pages"],

            images=message.get("images", []),

            generated_images=message.get("generated_images", [])

        )

question, uploaded_file = render_chat_input()

# ==========================================================
# Save Uploaded Image (only once per upload)
# ==========================================================

if (
    uploaded_file is not None
    and st.session_state.active_image is None
):

    file_identity = f"{uploaded_file.name}_{uploaded_file.size}"

    if file_identity != st.session_state.last_uploaded_file_id:

        suffix = os.path.splitext(uploaded_file.name)[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as tmp:

            tmp.write(uploaded_file.getbuffer())

            st.session_state.active_image = tmp.name

        st.session_state.active_image_name = uploaded_file.name
        st.session_state.last_uploaded_file_id = file_identity


if question:

    with st.chat_message("user"):

        st.markdown(question)

        image_placeholder = st.empty()

    pending_image_path = st.session_state.active_image
    pending_image_name = st.session_state.active_image_name

    with st.spinner("🤖 Thinking..."):

        start = time.time()

        final_state = None

        for step in ask_chatbot_stream(

            question,

            session_id=st.session_state.session_id,

            uploaded_image=st.session_state.active_image,

            uploaded_image_type=st.session_state.active_image_name,

        ):

            node_name, state_update = next(iter(step.items()))

            # -----------------------------------------
            # React the moment the router decides
            # -----------------------------------------

            if node_name == "router":

                route = state_update.get("route")

                if route == "vision" and pending_image_path:

                    image_placeholder.image(pending_image_path, width=250)

                else:

                    if pending_image_path and os.path.exists(pending_image_path):

                        os.remove(pending_image_path)

                    st.session_state.active_image = None
                    st.session_state.active_image_name = None
                    st.session_state.last_uploaded_file_id = None
                    st.session_state.upload_key += 1

                    pending_image_path = None
                    pending_image_name = None

            final_state = state_update

        end = time.time()

        elapsed = round(end - start, 2)

        result = final_state

        render_assistant_message(

            answer=result["answer"],

            agent=result["agent"],

            response_time=elapsed,

            context=result["context"],

            pages=result["pages"],

            images=result.get("images", []),

            generated_images=result.get("generated_images", [])

        )

    st.session_state.messages.append(

        {

            "role": "user",

            "content": question,

            "uploaded_image": pending_image_path,

            "uploaded_image_name": pending_image_name,

        }

    )

    st.session_state.messages.append(

        {

            "role": "assistant",

            "answer": result["answer"],

            "agent": result["agent"],

            "vision_model": result.get("vision_model", ""),

            "time": elapsed,

            "context": result["context"],

            "pages": result["pages"],

            "images": result.get("images", []),

            "generated_images": result.get("generated_images", [])

        }

    )
           