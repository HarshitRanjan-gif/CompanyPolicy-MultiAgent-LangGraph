import os

from dotenv import load_dotenv

from tavily import TavilyClient


# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()


# ==========================================================
# Tavily Client
# ==========================================================

client = TavilyClient(

    api_key=os.getenv("TAVILY_API_KEY")

)


# ==========================================================
# Search Function
# ==========================================================

def web_search(query: str):

    print("\n========== Web Search ==========")

    print(f"Searching : {query}")

    response = client.search(

        query=query,

        max_results=5

    )

    return response