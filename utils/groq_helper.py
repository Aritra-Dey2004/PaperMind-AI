import os
import importlib
from dotenv import load_dotenv

load_dotenv()


def _import_groq():
    try:
        mod = importlib.import_module("groq")
        # prefer attribute Groq if present
        Groq = getattr(mod, "Groq", None)
        if Groq is None:
            Groq = getattr(mod, "Client", None)
        return Groq
    except ModuleNotFoundError:
        return None


def generate_groq_answer(prompt):
    Groq = _import_groq()

    if Groq is None:
        raise ModuleNotFoundError(
            "groq package is not installed in the active environment. "
            "Install with: pip install groq"
        )

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env file.")

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful research paper assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=800
    )

    return response.choices[0].message.content