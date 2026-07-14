import os
import time

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
# Web Search
# ==========================================================

def web_search(
    query: str,
    retries: int = 2,
    timeout: int = 15,
    max_results: int = 5,
):
    """
    Perform a text-based web search using Tavily.

    Args:
        query: Search query.
        retries: Number of retry attempts.
        timeout: Timeout (seconds).
        max_results: Maximum search results.

    Returns:
        Tavily response dictionary.
    """

    print("\n========== Web Search ==========")
    print(f"Searching : {query}")

    for attempt in range(retries + 1):

        try:

            response = client.search(
                query=query,
                max_results=max_results,
                timeout=timeout,
            )

            return response

        except Exception as e:

            print(f"⚠️ Web search attempt {attempt + 1} failed: {e}")

            if attempt < retries:
                time.sleep(1)

    print("❌ Web search failed.")

    return {
        "results": []
    }