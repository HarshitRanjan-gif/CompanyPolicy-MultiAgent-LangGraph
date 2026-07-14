import os

import requests
import imagehash

from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
from serpapi import GoogleSearch

load_dotenv()

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

def get_image_hash(url: str):

    try:

        response = requests.get(

            url,

            timeout=5,

            headers={

                "User-Agent": "Mozilla/5.0"

            }

        )
        response.raise_for_status()

        img = Image.open(

            BytesIO(response.content)

        ).convert("RGB")

        return imagehash.phash(img)

    except Exception:

        return None
    

def google_image_search(
    request: dict,
    exclude_urls: set | None = None,
):
    """
    Search Google Images using SerpAPI.

    request example:

    {
        "query": "scarlett johansson",
        "count": 5,
        "transparent": False,
        "image_type": "photo"
    }
    """
    if exclude_urls is None:
        exclude_urls = set()

    query = request["query"]

    count = request.get("count", 1)

    transparent = request.get("transparent", False)

    image_type = request.get("image_type", "photo")

    params = {

        "engine": "google_images",

        "q": query,

        "api_key": SERPAPI_API_KEY,

        "safe": "active",

        "ijn": 0,

        # Google returns 100 max
        "num": min(max(count * 6, 20), 100),

    }

    # -----------------------------------------
    # Transparent PNG
    # -----------------------------------------

    if transparent:

        params["tbs"] = "ic:trans"

    # -----------------------------------------
    # Wallpaper / Large Images
    # -----------------------------------------

    elif image_type == "wallpaper":

        params["tbs"] = "isz:l"

    # -----------------------------------------
    # Portrait / Face
    # -----------------------------------------

    elif image_type == "portrait":

        params["tbs"] = "itp:face"

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
    except Exception as e:
        print(f"SerpAPI Error: {e}")
        return []

    results = search.get_dict()

    images = []

    seen_hashes = set()

    seen_urls = set()

    for item in results.get("images_results", []):

        url = item.get("original") or item.get("thumbnail")

        if not url:
            continue

        if url in exclude_urls:
            print("⏭ Skipped (already shown)")
            continue

        if url in seen_urls:
            continue

        img_hash = get_image_hash(url)

        if img_hash is None:
            continue

        duplicate = False

        for existing_hash in seen_hashes:

            # Hamming distance
            if img_hash - existing_hash <= 5:

                duplicate = True

                break

        if duplicate:
            print("⏭ Skipped (similar image)")
            continue

        seen_hashes.add(img_hash)   

        seen_urls.add(url)

        print("\n----------------------------")
        print("Title :", item.get("title"))
        print("Source:", item.get("source"))
        print("URL   :", item.get("original"))

        images.append(url)

        if len(images) >= count:
            break

    return images