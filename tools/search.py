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
# Text Search Function
# ==========================================================

def web_search(query: str, retries: int = 2, timeout: int = 15):

    print("\n========== Web Search ==========")

    print(f"Searching : {query}")

    for attempt in range(retries + 1):

        try:

            response = client.search(

                query=query,

                max_results=5,

                timeout=timeout

            )

            return response

        except Exception as e:

            print(f"⚠️ Web search attempt {attempt + 1} failed: {e}")

            if attempt < retries:

                time.sleep(1)

            else:

                print("❌ All web search attempts failed. Returning empty results.")

                return {"results": []}


# ==========================================================
# Image Search Function
# ==========================================================

def image_search(query: str, retries: int = 2, timeout: int = 15, max_images: int = 4):

    print("\n========== Image Search ==========")

    print(f"Searching Images : {query}")

    for attempt in range(retries + 1):

        try:

            response = client.search(

                query=query,

                max_results=5,

                include_images=True,

                timeout=timeout

            )

            images = response.get("images", [])[:max_images]

            return images

        except Exception as e:

            print(f"⚠️ Image search attempt {attempt + 1} failed: {e}")

            if attempt < retries:

                time.sleep(1)

            else:

                print("❌ All image search attempts failed. Returning empty list.")

                return []