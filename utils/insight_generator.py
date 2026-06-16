def generate_insight(model, text, insight_type):
    prompt = f"""
You are a research paper assistant.

From the following research paper, generate only the section requested.

Requested section:
{insight_type}

Research Paper:
{text[:12000]}

Give the answer in clear bullet points.
"""

    response = model.generate_content(prompt)
    return response.text