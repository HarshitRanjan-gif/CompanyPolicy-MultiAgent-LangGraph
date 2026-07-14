from utils.image_request_parser import parse_image_request
from tools.serpapi_client import google_image_search


# ==========================================================
# Parse Image Request
# ==========================================================

def parse_request(question: str):

    return parse_image_request(question)


# ==========================================================
# Image Search
# ==========================================================

def image_search(
    question: str,
    exclude_urls: set | None = None,
):

    if exclude_urls is None:
        exclude_urls = set()

    print("\n========== Image Search ==========")
    print(f"User Request : {question}")

    # -----------------------------------------
    # Parse the request
    # -----------------------------------------

    request = parse_image_request(question)

    print("\nParsed Request")

    for k, v in request.items():
        print(f"{k}: {v}")

    # -----------------------------------------
    # Search Images
    # -----------------------------------------

    images = google_image_search(
        request,
        exclude_urls=exclude_urls,
    )

    print(f"\nReturned {len(images)} images")

    return {
        "query": request["query"],
        "images": images,
    }