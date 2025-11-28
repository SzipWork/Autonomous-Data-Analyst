import pandas as pd
from app.utils.gemini_client import GeminiClient


class ChatAgent:
    def __init__(self):
        self.gemini = GeminiClient()

    def _build_context(self, df: pd.DataFrame) -> str:
        """
        Builds a safe, compact summary of the dataset
        to send to Gemini.
        """

        context_parts = []

        # Basic shape
        context_parts.append(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

        # Column info
        context_parts.append(f"Columns: {list(df.columns)}")

        # Data types
        dtypes = df.dtypes.astype(str).to_dict()
        context_parts.append(f"Column Types: {dtypes}")

        # Summary statistics
        try:
            summary = df.describe(include="all").to_string()
            context_parts.append(f"Summary Statistics:\n{summary}")
        except Exception:
            pass

        # Show first 10 rows (safe preview)
        preview = df.head(10).to_string()
        context_parts.append(f"Sample Data (first 10 rows):\n{preview}")

        return "\n\n".join(context_parts)

    def answer_question(self, df: pd.DataFrame, question: str) -> str:
        """
        Uses Gemini to answer ANY user question based on dataset context.
        """

        context = self._build_context(df)

        try:
            answer = self.gemini.ask(question, context=context)
            return answer or "I could not generate a response."
        except Exception as e:
            return f"Error while generating answer: {str(e)}"
