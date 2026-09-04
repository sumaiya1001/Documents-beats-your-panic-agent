import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("ERROR: GEMINI_API_KEY not found. Check your .env file.")
else:
    print("Key loaded successfully. Testing Gemini API call...")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents="Say hello in exactly 5 words."
    )
    print("Gemini says:", response.text)