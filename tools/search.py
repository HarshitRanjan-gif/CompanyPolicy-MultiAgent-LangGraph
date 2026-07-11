import os
import time
from urllib.parse import urlparse
import re
import requests
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
# Text Search
# ==========================================================

def web_search(query: str, retries: int = 2, timeout: int = 15):

    print("\n========== Web Search ==========")
    print(f"Searching : {query}")

    for attempt in range(retries + 1):

        try:

            return client.search(
                query=query,
                max_results=5,
                timeout=timeout,
            )

        except Exception as e:

            print(f"⚠️ Web search attempt {attempt + 1} failed: {e}")

            if attempt < retries:
                time.sleep(1)

    print("❌ Web search failed.")

    return {"results": []}


# ==========================================================
# URL Normalization
# ==========================================================

def normalize_url(url: str):

    parsed = urlparse(url)

    filename = os.path.basename(parsed.path).lower()

    # --------------------------------------------------
    # Remove common image transformation suffixes
    # --------------------------------------------------

    filename = re.sub(r"\._.*?(?=\.)", "", filename)

    # --------------------------------------------------
    # Remove query parameters
    # --------------------------------------------------

    filename = filename.split("?")[0]

    return (
        parsed.netloc.lower(),
        filename,
    )

# ==========================================================
# Validate Image URL
# ==========================================================

def is_valid_image(url: str, timeout: int = 5):

    try:

        response = requests.get(
            url,
            stream=True,
            timeout=timeout,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
        )

        if response.status_code != 200:
            return False

        content_type = response.headers.get(
            "Content-Type",
            ""
        ).lower()

        return content_type.startswith("image/")

    except Exception:

        return False


# ==========================================================
# Image Ranking Score
# ==========================================================

def image_score(url: str):

    url = url.lower()

    score = 100

    # ------------------------------------------------------
    # High-quality portrait/photo keywords
    # ------------------------------------------------------

    positive = {

        "portrait": 40,
        "headshot": 35,
        "photo": 20,
        "photos": 20,
        "actor": 15,
        "actress": 15,
        "celeb": 15,
        "celebs": 15,
        "festival": 20,
        "cannes": 20,
        "red-carpet": 20,
        "press": 15,
        "official": 20,
        "wikimedia": 15,
        "wikipedia": 15,
        "tmdb": 20,
    }

    # ------------------------------------------------------
    # Lower-quality image keywords
    # ------------------------------------------------------

    negative = {

        "poster": -60,
        "movie": -35,
        "film": -35,
        "dvd": -40,
        "cover": -40,
        "wallpaper": -40,
        "banner": -40,
        "marvel": -20,
        "avengers": -25,
        "dc": -20,
        "header": -40,
        "footer": -40,
        "theme": -40,
        "icon": -60,
        "logo": -60,
        "thumbnail": -25,
        "thumb": -25,
        "scene": -35,
        "frame": -35,
        "screenshot": -30,
    }

    for word, value in positive.items():

        if word in url:

            score += value

    for word, value in negative.items():

        if word in url:

            score += value

    return score

# ==========================================================
# Image Search
# ==========================================================

def image_search(
    query: str,
    retries: int = 2,
    timeout: int = 15,
    max_images: int = 8,
):

    print("\n========== Image Search ==========")
    print(f"Searching Images : {query}")

    skip_patterns = [
        
        "pinimg",
        "pinterest",
        "hairstyle"
        "hair",
        "makeup",
        "fashion",


        # Logos / Icons
        "logo",
        "logos",
        "icon",
        "icons",
        ".svg",
        "favicon",

        # Placeholders
        "placeholder",
        "avatar",
        "default",

        # Stock Images
        "getty",
        "alamy",
        "shutterstock",
        "istock",
        "depositphotos",
        "dreamstime",

        # Small thumbnails
        "thumb",
        "thumbnail",
        "sprite",
        "px-",

        # Unwanted
        "crossword",
        "games-assets",

        # Website UI
        "header",
        "footer",
        "banner",
        "nav",
        "menu",

        # Generic assets
        "biography.png",
        "blank",
        "loading",
        "spinner",

        # Theme assets
        "theme",
        "wp-content/themes",
        "assets/images",
        "icons",
        "button",

        # Tracking beacon
        "scorecardresearch",
        "doubleclick",
        "googletagmanager",
        "google-analytics",
        "pixel",
        "tracking",
        "analytics",
        "beacon",


    ]

    query_words = [

        word.lower()

        for word in query.split()

        if len(word) > 2

    ]

    for attempt in range(retries + 1):

        try:

            response = client.search(

                query=query,

                include_images=True,

                search_depth="advanced",

                # Increased from 8 → 12
                max_results=12,

                timeout=timeout,

            )

            candidate_images = []

            # ======================================================
            # Global Tavily Images
            # ======================================================

            candidate_images.extend(

                response.get("images", [])

            )

            # ======================================================
            # Images from relevant search results
            # ======================================================

            for result in response.get("results", []):

                title = result.get("title", "").lower()

                content = result.get("content", "").lower()

                searchable_text = f"{title} {content}"

                if query_words:

                    matches = sum(

                        word in searchable_text

                        for word in query_words

                    )

                    if matches < max(1, len(query_words) // 2):

                        continue

                candidate_images.extend(

                    result.get("images", [])[:3]

                )

            # ======================================================
            # Remove duplicate candidates
            # ======================================================

            unique_candidates = []

            seen_candidates = set()

            for img in candidate_images:

                if not img:
                    continue

                key = normalize_url(img)

                if key in seen_candidates:
                    continue

                seen_candidates.add(key)

                unique_candidates.append(img)

            print(f"Found {len(unique_candidates)} unique candidates")


            # ======================================================
            # Rank candidates before validation
            # ======================================================

            unique_candidates = sorted(
                unique_candidates,
                key=image_score,
                reverse=True
            )

            # ======================================================
            # Validate Images
            # ======================================================

            images = []

            seen_final = set()

            checked = 0

            for img_url in unique_candidates:

                checked += 1

                lower = img_url.lower()

                if any(pattern in lower for pattern in skip_patterns):

                    continue

                key = normalize_url(img_url)

                if key in seen_final:

                    continue

                print(f"Checking candidate {checked}/{len(unique_candidates)}")

                if not is_valid_image(img_url):

                    print("❌ Broken")

                    continue

                print("✅ Valid")

                seen_final.add(key)

                images.append(img_url)

                # Return 8 working images instead of stopping at 4
                if len(images) >= max_images:

                    break

            print(f"Returning {len(images)} working images")

            print("\n========== Returned Images ==========")

            for i, img in enumerate(images):
                print(f"{i+1}. {img}")

            return images

        except Exception as e:

            print(f"⚠️ Image search attempt {attempt + 1} failed: {e}")

            if attempt < retries:

                time.sleep(1)

    print("❌ Image search failed.")

    return []