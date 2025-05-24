import os
from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_ID = "gemini-2.5-flash-preview-05-20"

client = genai.Client(api_key=GEMINI_API_KEY)

def get_gpt():
    return client.models.get(MODEL_ID)
