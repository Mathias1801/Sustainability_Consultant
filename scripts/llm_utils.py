import os
from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY environment variable not found")

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_response(prompt: str, model: str = "gemini-2.5-flash-preview-05-20"):
    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )
    return response.text
