import os

import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not set. "
    )

genai.configure(api_key=GEMINI_API_KEY)


generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 100,
    "max_output_tokens": 32768,
}


model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)