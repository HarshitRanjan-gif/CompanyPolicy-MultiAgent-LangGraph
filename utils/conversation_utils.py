# ==========================================================
# Conversation Utilities
# ==========================================================

CONTROL_RESPONSES = {

    "ok": "Glad I could help!",

    "okay": "Glad I could help!",

    "ok good": "Glad I could help!",

    "good": "Happy to help!",

    "great": "Glad to hear that!",

    "nice": "I'm happy that helped!",

    "awesome": "Glad to hear that!",

    "cool": "Great!",

    "thanks": "You're welcome!",

    "thank you": "You're welcome!",

    "bye": "Goodbye! Have a great day!",

    "goodbye": "Goodbye! Have a great day!",

    "stop": "Alright! If you need anything else, just let me know.",

    "exit": "Alright! Have a great day!",

    "quit": "Goodbye!"

}


def get_control_response(text: str):

    return CONTROL_RESPONSES.get(

        text.strip().lower()

    )