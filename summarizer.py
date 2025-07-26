import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key = os.getenv("GEMINI_API_KEY"))


model = genai.GenerativeModel("models/gemini-2.5-flash")

def summarize_text(text : str) -> str:
    prompt = f"Summarize the following academic abstract in simple, clear language if no proper research papers are found simple stop without repeating the previously added papers: \n\n{text}"
    response = model.generate_content(prompt)
    return response.text.strip()

 
    