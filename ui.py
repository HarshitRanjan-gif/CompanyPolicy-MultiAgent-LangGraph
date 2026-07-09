import streamlit as st


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

        st.markdown("---")

        st.subheader("⚙️ Tech Stack")

        st.write("📚 FAISS Vector Store")
        st.write("🤗 BGE-M3 Embeddings")
        st.write("🌐 Tavily Search")
        st.write("⚡ Groq Llama 3.3")
        st.write("🧠 LangGraph Memory")

        st.markdown("---")

        if st.button("🗑 Clear Conversation"):

            st.session_state.messages = []

            st.rerun()


# ==========================================================
# Header
# ==========================================================

def render_header():

    st.markdown(
"""<div style="text-align:center; padding-top:40px;">

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

def render_user_message(message):

    with st.chat_message("user"):

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

    images=None

):

    # -----------------------------------------
    # Agent Badge Color
    # -----------------------------------------

    if agent == "RAG Agent":

        color = "#1976D2"
        icon = "🔵"

    elif agent == "Web Search Agent":

        color = "#FB8C00"
        icon = "🟠"

    elif agent == "LLM Agent":

        color = "#8E24AA"
        icon = "🟣"

    elif agent == "Router Agent":

        color = "#2E7D32"
        icon = "🟢"

    else:

        color = "#455A64"
        icon = "⚪"

    with st.chat_message("assistant"):

        st.markdown(answer)

        # -----------------------------------------
        # Display Images
        # -----------------------------------------

        if images:

            cols = st.columns(len(images))

            for col, img_url in zip(cols, images):

                with col:

                    st.image(img_url, use_container_width=True)

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

        st.caption(

            f"⏱ Response Time : {response_time} sec"

        )

        if pages:

            st.write("### 📄 Source Pages")

            st.write(

                ", ".join(

                    f"Page {page}"

                    for page in pages

                )

            )

        if context:

            with st.expander("📚 Retrieved Context"):

                st.write(context)