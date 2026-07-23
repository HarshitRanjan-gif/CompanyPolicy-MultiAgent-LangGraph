import streamlit as st
import os

# ==========================================================
# Sidebar
# ==========================================================

def render_sidebar():

    with st.sidebar:

        st.title("🤖 Company AI Assistant")

        st.markdown("---")

        st.subheader("🧠 Multi-Agent System")

        st.success("🟢 Router Agent")
        st.info("🔵 RAG Agent")
        st.warning("🟠 Web Search Agent")
        st.error("🟣 LLM Agent")
        st.info("🖼️ Image Agent")
        st.success("🎨 Image Generation Agent")

        st.markdown("---")

        st.subheader("⚙️ Tech Stack")

        st.write("📚 FAISS Vector Store")
        st.write("🤗 BGE-M3 Embeddings")
        st.write("🌐 Tavily Search")
        st.write("🖼️ SerpAPI (Image Search)")
        st.write("👁️ Qwen2.5-VL (Image Analysis)")
        st.write("🎨 OpenAI Images (Image Generation)")
        st.write("⚡ Groq Llama 3.3")
        st.write("🧠 LangGraph")

        st.markdown("---")

        if st.button("🗑 Clear Conversation"):

            st.session_state.messages = []

            st.session_state.active_image = None
            st.session_state.active_image_name = None
            st.session_state.last_uploaded_file_id = None

            st.session_state.upload_key += 1



# ==========================================================
# Header
# ==========================================================

def render_header():

    st.markdown(
"""
<div style="text-align:center; padding-top:40px;">

<h1 style="font-size:58px; color:white;">
🤖 Company AI Assistant
</h1>

<p style="font-size:22px; color:#A0A0A0;">
Multi-Agent AI powered by LangGraph
</p>

</div>
""",
        unsafe_allow_html=True,
    )

    st.divider()


# ==========================================================
# User Message
# ==========================================================

# ==========================================================
# User Message
# ==========================================================

def render_user_message(message, image_path=None):

    with st.chat_message("user"):

        if image_path and os.path.exists(image_path):

            st.image(image_path, width=250)

        st.markdown(message)


# ==========================================================
# Assistant Message
# ==========================================================

def render_assistant_message(

    answer,

    agent,

    response_time,

    context="",

    pages=None,

    images=None,

    generated_images=None

):

    # ==========================================================
    # Agent Badge Color
    # ==========================================================

    if agent == "Router Agent":

        color = "#2E7D32"      # Green
        icon = "🟢"

    elif agent == "RAG Agent":

        color = "#1976D2"      # Blue
        icon = "📚"

    elif agent == "Web Search Agent":

        color = "#FB8C00"      # Orange
        icon = "🌐"

    elif agent == "Image Agent":

        color = "#0097A7"      # Cyan
        icon = "🖼️"

    elif agent == "Image Generation Agent":

        color = "#8E24AA"      # Purple
        icon = "🎨"

    elif agent == "LLM Agent":

        color = "#D81B60"      # Pink
        icon = "🧠"

    else:

        color = "#455A64"
        icon = "⚪"

    with st.chat_message("assistant"):

        st.markdown(answer)

        # ======================================================
        # Display Images
        # ======================================================

        if images:

            print("\n========== UI Images ==========")

            for i, img in enumerate(images, 1):
                print(f"{i}. {img}")

            # Remove duplicate URLs
            images = list(dict.fromkeys(images))

            MAX_COLUMNS = 4

            # Display images in rows of 4
            for i in range(0, len(images), MAX_COLUMNS):

                row = images[i:i + MAX_COLUMNS]

                cols = st.columns(4)

                for col, img in zip(cols, row):

                    with col:

                        try:

                            st.image(
                            img,
                            width=250,
                        )

                        except Exception:

                            continue

        # ======================================================
        # Display Generated Images
        # ======================================================

        if generated_images:

            print("\n========== Generated Images ==========")

            for i, img in enumerate(generated_images, 1):
                print(f"{i}. {img}")

            for img_url in generated_images:

                try:

                    st.image(img_url, width=400)

                except Exception:

                    continue

        # ======================================================
        # Agent Badge
        # ======================================================

        st.markdown(

            f"""
            <div style="
                background:{color};
                padding:12px;
                border-radius:10px;
                margin-top:12px;
                margin-bottom:12px;
                color:white;
                font-weight:bold;
                text-align:center;
            ">
                {icon} Answered By : {agent}
            </div>
            """,

            unsafe_allow_html=True

        )

        # ======================================================
        # Response Time
        # ======================================================

        st.caption(

            f"⏱ Response Time : {response_time:.2f} sec"

        )

        # ======================================================
        # Source Pages
        # ======================================================

        if pages:

            st.write("### 📄 Source Pages")

            st.write(

                ", ".join(

                    f"Page {page}"

                    for page in pages

                )

            )

        # ======================================================
        # Retrieved Context
        # ======================================================

        if context:

            with st.expander("📚 Retrieved Context"):

                st.write(context)

# ==========================================================
# Chat Input
# ==========================================================

def render_chat_input():

    prompt = st.chat_input(
        "Ask anything...",
        accept_file=True,
        file_type=["png", "jpg", "jpeg", "webp"],
        key="main_chat_input",
    )

    if prompt is None:

        return None, None

    question = prompt.text if prompt.text else None

    uploaded_file = None

    if prompt["files"]:

        uploaded_file = prompt["files"][0]

    return question, uploaded_file