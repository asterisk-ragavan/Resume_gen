from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

def test_model():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("GOOGLE_API_KEY not found in environment.")
        return

    client = genai.Client(api_key=api_key)
    try:
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents="Hello, are you Gemini 3?"
        )
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_model()
