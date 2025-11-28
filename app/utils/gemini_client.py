# app/utils/gemini_client.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load .env
load_dotenv()

class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("Missing GOOGLE_API_KEY in .env file")

        # Pass API key to the Gemini model
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            temperature=0.2,
            max_output_tokens=2048,
            google_api_key=api_key
        )

    def ask(self, message: str, context: str = "") -> str:
        prompt = (
            "You are a data analysis assistant.\n"
            "Answer ONLY based on the dataset context provided.\n\n"
            f"DATASET CONTEXT:\n{context}\n\n"
            f"USER QUESTION:\n{message}\n\n"
        )

        response = self.model.invoke(prompt)
        return response.content
