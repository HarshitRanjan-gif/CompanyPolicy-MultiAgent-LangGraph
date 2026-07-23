import urllib.parse
import random


# ==========================================================
# Image Generation (Pollinations.ai - free, no API key)
# ==========================================================

def generate_image(prompt: str, width: int = 768, height: int = 768) -> str:

    encoded_prompt = urllib.parse.quote(prompt)

    seed = random.randint(1, 999999)

    url = (
        f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        f"?width={width}&height={height}&nologo=true&seed={seed}"
    )

    return url