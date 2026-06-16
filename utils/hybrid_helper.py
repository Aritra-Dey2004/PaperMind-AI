from utils.groq_helper import generate_groq_answer
from utils.ollama_helper import generate_ollama_answer

def _fallback_response(prompt, fallback_query):
    try:
        answer = generate_groq_answer(prompt)
        return answer, "Groq"
    except Exception:
        answer = generate_ollama_answer(fallback_query, prompt)
        return answer, "Ollama Local Fallback"


def generate_hybrid_response(gemini_model, prompt, fallback_query="Generate response"):
    if gemini_model is None:
        return _fallback_response(prompt, fallback_query)

    try:
        if hasattr(gemini_model, "generate_content"):
            response = gemini_model.generate_content(prompt)
            return response.text, "Gemini"

        if hasattr(gemini_model, "generate"):
            response = gemini_model.generate(prompt=prompt)
            return getattr(response, "text", getattr(response, "content", str(response))), "Gemini"

    except Exception:
        pass

    return _fallback_response(prompt, fallback_query)