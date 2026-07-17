import os

from dotenv import load_dotenv
from google import genai
from PIL import Image

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# ==========================================================
# Image Analysis
# ==========================================================

def analyze_image(
    image_path: str,
    question: str = "",
):
    """
    Analyze an image using Gemini Vision.
    """

    try:

        image = Image.open(image_path)

    except Exception as e:

        return f"Unable to open image.\n\n{e}"

    # -----------------------------------------
    # Default Prompt
    # -----------------------------------------

    if not question.strip():

        question = (
            "Describe this image in as much detail as possible. "
            "Identify people, objects, text, locations, colors, "
            "activities and anything important."
        )

    try:

        response = client.models.generate_content(

            model="models/gemini-3.5-flash",

            contents=[
                question,
                image,
            ],
        )

        return response.text

    except Exception as e:

        return f"Gemini Vision Error:\n\n{e}"