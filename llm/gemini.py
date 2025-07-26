import google.generativeai as genai
import os

# Configure the Gemini API key
# Make sure to set the GOOGLE_API_KEY environment variable in your system
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

def generate_text(prompt):
    """Generates text using the Gemini API."""
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    return response.text
