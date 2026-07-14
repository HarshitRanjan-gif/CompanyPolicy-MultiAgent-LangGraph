import re


NUMBER_WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
}


def parse_image_request(question: str) -> dict:
    """
    Parse an image request.

    Returns:
    {
        "query": "...",
        "count": 1,
        "transparent": False,
        "type": "photo"
    }
    """

    q = question.lower()

    # -----------------------------
    # Default values
    # -----------------------------

    count = 1
    transparent = False
    image_type = "photo"

    # -----------------------------
    # Number
    # -----------------------------

    match = re.search(r"\b(\d+)\b", q)

    if match:
        count = max(1, min(int(match.group(1)), 10))

    else:

        for word, value in NUMBER_WORDS.items():

            if re.search(rf"\b{word}\b", q):

                count = value
                break

    # -----------------------------
    # Transparent PNG
    # -----------------------------

    if "transparent" in q or "png" in q:

        transparent = True

    # -----------------------------
    # Wallpapers
    # -----------------------------

    if "wallpaper" in q:

        image_type = "wallpaper"

    # -----------------------------
    # Portrait
    # -----------------------------

    elif "portrait" in q:

        image_type = "portrait"

    # -----------------------------
    # Extract subject
    # -----------------------------

    patterns = [

        r".*?(?:picture|image|photo|photograph|pic)s?\s+of\s+",

        r".*?show\s+me\s+(?:\d+\s+)?(?:pictures|images|photos|pics)?\s*of\s+",

        r".*?give\s+me\s+(?:\d+\s+)?(?:pictures|images|photos|pics)?\s*of\s+",

        r".*?find\s+(?:\d+\s+)?(?:pictures|images|photos|pics)?\s*of\s+",

    ]

    subject = q

    for pattern in patterns:

        subject = re.sub(pattern, "", subject)

    subject = subject.strip(" ?.!")

    return {

        "query": subject,

        "count": count,

        "transparent": transparent,

        "image_type": image_type,

    }