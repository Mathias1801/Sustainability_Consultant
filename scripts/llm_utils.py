import os
from google import genai

# Load API key from environment variable
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_ID = "gemini-2.5-flash-preview-05-20"

# Configure the Gemini client
genai.configure(api_key=GOOGLE_API_KEY)

def get_gpt():
    return genai.GenerativeModel(model_name=MODEL_ID)
