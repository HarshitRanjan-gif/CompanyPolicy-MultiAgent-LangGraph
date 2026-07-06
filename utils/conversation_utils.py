import random
import re

# ==========================================================
# Conversation Utilities
# ==========================================================

import random

CONVERSATION_RESPONSES = {

    # Greetings
    "hi": [
        "Hello! 👋 How can I help you today?",
        "Hi there! 😊 What can I assist you with today?",
        "Hello! It's great to see you. How can I help?"
    ],

    "hello": [
        "Hello! 👋 How can I help you today?",
        "Hi! 😊 What would you like to know?",
        "Hello! What can I do for you today?"
    ],

    "hey": [
        "Hey! 👋 How can I assist you today?",
        "Hi! What can I help you with today?"
    ],

    "hii": [
        "Hello! 👋 How can I help you today?",
        "Hi there! 😊"
    ],

    "hellow": [
        "Hello! 👋 How can I help you today?",
        "Hi! 😊 What can I do for you today?"
    ],

    "good morning": [
        "Good morning! ☀️ Hope you're having a great day!",
        "Good morning! How can I assist you today?"
    ],

    "good afternoon": [
        "Good afternoon! 😊 How can I help you today?"
    ],

    "good evening": [
        "Good evening! 🌙 What can I do for you today?"
    ],

    # Acknowledgements
    "ok": [
        "Glad I could help!",
        "Alright! 😊"
    ],

    "okay": [
        "Glad I could help!",
        "Sounds good!"
    ],

    "ok good": [
        "I'm glad to hear that! 😊"
    ],

    "good": [
        "Happy to help!",
        "Glad I could help!"
    ],

    "great": [
        "That's great! 😊",
        "Glad to hear that!"
    ],

    "nice": [
        "I'm happy that helped!",
        "😊 Glad you liked it!"
    ],

    "awesome": [
        "Awesome! 🚀",
        "Glad to hear that!"
    ],

    "cool": [
        "😄 Great!",
        "Happy to help!"
    ],

    # Thanks
    "thanks": [
        "You're welcome! 😊",
        "Happy to help!"
    ],

    "thank you": [
        "You're welcome! 😊",
        "My pleasure!"
    ],

    # Goodbye
    "bye": [
        "Goodbye! 👋 Have a great day!",
        "See you next time!"
    ],

    "goodbye": [
        "Goodbye! 👋 Have a wonderful day!"
    ],

    "stop": [
        "Alright! If you need anything else later, just let me know."
    ],

    "exit": [
        "Have a great day! 👋"
    ],

    "quit": [
        "Goodbye! 👋"
    ]
}

# ==========================================================
# Normalize Text
# ==========================================================

def normalize_text(text: str):

    text = text.strip().lower()

    # Reduce repeated characters
    # hiiii -> hi
    # heyyyy -> hey
    # helloooo -> hello

    text = re.sub(r'(.)\1{2,}', r'\1', text)

    return text


def get_control_response(text: str):

    text = normalize_text(text)

    if text in CONVERSATION_RESPONSES:

        return random.choice(CONVERSATION_RESPONSES[text])

    return None