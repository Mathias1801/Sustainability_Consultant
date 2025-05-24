import os
from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY environment variable not found")

client = genai.Client(api_key=GEMINI_API_KEY)

def get_gpt():
    return client.get_model("gemini-2.5-flash-preview-05-20")
