import importlib
import os
from dotenv import load_dotenv

load_dotenv()


def _import_gemini_module():
    for module_name in ["google.genai", "google.generativeai"]:
        try:
            return importlib.import_module(module_name)
        except ModuleNotFoundError:
            continue

    raise ModuleNotFoundError(
        "Neither google.genai nor google.generativeai is installed. "
        "Install one of these packages to enable Gemini support."
    )


def setup_gemini():
    genai = _import_gemini_module()
    api_key = os.getenv("GOOGLE_API_KEY")

    if api_key is None or api_key.strip() == "":
        raise EnvironmentError(
            "GOOGLE_API_KEY is not set. Please add it to your environment or .env file."
        )

    if hasattr(genai, "configure"):
        genai.configure(api_key=api_key)
        return genai.GenerativeModel("models/gemini-2.5-flash")

    if hasattr(genai, "GenerativeModel"):
        return genai.GenerativeModel("models/gemini-2.5-flash")

    if hasattr(genai, "Client"):
        client = genai.Client(api_key=api_key)
        return client

    raise RuntimeError(
        "Installed Gemini package does not expose a known client interface."
    )


def generate_answer(model, query, context):
    prompt = f"""
You are a research paper assistant.

Use only the provided context to answer the question.

Context:
{context}

Question:
{query}

Answer:
"""

    if hasattr(model, "generate_content"):
        response = model.generate_content(prompt)
        return getattr(response, "text", str(response))

    if hasattr(model, "generate"):
        response = model.generate(prompt=prompt)
        return getattr(response, "text", getattr(response, "content", str(response)))

    raise RuntimeError(
        "The Gemini model object does not support generate_content or generate()."
    )
