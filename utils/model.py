import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not set. "
        "Create a .env file and add GEMINI_API_KEY."
    )


GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash",
)


client = genai.Client(
    api_key=GEMINI_API_KEY,
)


class GeminiModel:
    """
    Compatibility wrapper for the existing application.

    Preserves:
        model.start_chat(history=[])
    """

    def start_chat(self, history=None):
        return client.chats.create(
            model=GEMINI_MODEL,
            history=history or [],
        )


model = GeminiModel()