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

        img = Image.open(BytesIO(response.content)).convert("RGB")

        # ----------------------------------------------------
        # Reject extreme aspect ratios
        # ----------------------------------------------------

        width, height = img.size

        if height == 0:
            return None

        ratio = width / height

        if ratio < 0.4 or ratio > 2.5:

            print("⏭ Skipped (extreme aspect ratio)")

            return None

        return imagehash.phash(img)

    except Exception:

        return None
    
def is_valid_image_url(url: str) -> bool:

    try:

        response = requests.get(

            url,

            timeout=5,

            stream=True,

            headers={

                "User-Agent": "Mozilla/5.0"

            }

        )

        print(
            url,
            response.status_code,
            response.headers.get("Content-Type")
        )

        if response.status_code != 200:

            return False

        content_type = response.headers.get(
            "Content-Type",
            ""
        ).lower()

        return content_type.startswith("image/")

    except Exception as e:

        print("URL ERROR:", e)

        return False    

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

    images = []

    seen_hashes = set()

    seen_urls = set()

    for item in results.get("images_results", []):

        source = (item.get("source") or "").lower()

        trusted_sources = {
            "wikipedia",
            "simple wikipedia",
            "imdb",
            "britannica",
            "mubi",
            "golden globes",
            "getty images",
            "people",
            "ap news",
            "reuters",
        }

        blocked_sources = {
            "instagram",
            "facebook",
            "pinterest",
            "fandom",
            "wikia",
            "reddit",
        }

        if any(site in source for site in blocked_sources):

            print(f"⏭ Skipped (blocked source: {source})")

            continue

        url = item.get("original") or item.get("thumbnail")

        if not url:
            continue

        if not is_valid_image_url(url):
            print("⏭ Skipped (malformed URL)")
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