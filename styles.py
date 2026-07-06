import streamlit as st


def load_css():

    st.markdown(
        """
        <style>

        /* Main Background */

        .stApp{
            background-color:#0E1117;
            color:white;
        }


        /* Chat Input */

        .stChatInput{
            padding-top:15px;
        }


        /* Sidebar */

        section[data-testid="stSidebar"]{
            background:#161B22;
        }


        /* Headers */

        h1,h2,h3{
            color:white;
        }


        /* Agent Badge */

        .agent-box{

            background:#1F2937;

            border-left:6px solid #00C853;

            padding:12px;

            border-radius:10px;

            margin-top:10px;

            margin-bottom:10px;

            color:white;

            font-weight:bold;

        }


        /* Response Info */

        .info-box{

            background:#1A1A1A;

            border-radius:10px;

            padding:10px;

            margin-top:10px;

        }


        /* Expander */

        div[data-testid="stExpander"]{

            border-radius:12px;

        }


        /* Scroll Bar */

        ::-webkit-scrollbar{
            width:8px;
        }

        ::-webkit-scrollbar-thumb{

            background:#444;

            border-radius:10px;

        }

        </style>
        """,
        unsafe_allow_html=True
    )