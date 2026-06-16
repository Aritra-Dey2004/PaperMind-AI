import requests

def generate_ollama_answer(query, context, model_name="llama3.2"):
    prompt = f"""
You are a research paper assistant.

Use only the provided context to answer the question.

Context:
{context}

Question:
{query}

Answer:
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model_name,
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]