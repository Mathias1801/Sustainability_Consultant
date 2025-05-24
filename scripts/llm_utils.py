import os
from google import genai

# Retrieve the API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY or GOOGLE_API_KEY environment variable not found")

# Initialize the GenAI client
client = genai.Client(api_key=GEMINI_API_KEY)

def get_gpt():
    # Access the desired model using the client
    return client.models.get_model("gemini-2.5-flash-preview-05-20")
