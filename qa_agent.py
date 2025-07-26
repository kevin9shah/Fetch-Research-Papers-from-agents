import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("models/gemini-2.5-flash")

def answer_question(question : str, context : str) -> str:
    prompt = f"""You are a research assistant.
You will be given several simplified academic paper summaries, and a user's question.
Answer the question based ONLY on the summaries provided.

--- Summaries ---
{context}

--- Question ---
{question}

Answer:"""

    response = model.generate_content(prompt)
    return response.text