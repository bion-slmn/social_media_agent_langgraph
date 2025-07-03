import os
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Optional
import logging
from dotenv import load_dotenv
load_dotenv()

def load_model(model: str) -> Optional[ChatGoogleGenerativeAI]:
    """
    Load a Gemini model using ChatGoogleGenerativeAI.

    Args:
        model (str): The name of the Gemini model to load.

    Returns:
        ChatGoogleGenerativeAI: The loaded model instance, or None if an error occurs.
    """
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")
    llm = ChatGoogleGenerativeAI(
            model=model,
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )
    return llm

