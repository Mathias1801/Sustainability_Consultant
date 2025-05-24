import os
from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY environment variable not found")

genai.configure(api_key=GEMINI_API_KEY)

def get_gpt():
    return genai.GenerativeModel(model_name="gemini-2.5-flash-preview-05-20")
