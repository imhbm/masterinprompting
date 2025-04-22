import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is loaded
if not gemini_api_key:
    raise ValueError("Gemini API key not found in .env file")

# Configure Gemini API
genai.configure(api_key=gemini_api_key)

# Set up the model
model = genai.GenerativeModel('gemini-2.0-flash-001')

# Generate content
prompt = "why sky is blue?"
response = model.generate_content(prompt)

# Print the response
print(response.text)