def generate_summary(model, text):

    prompt = f"""
    Summarize the following research paper.

    Provide:
    1. Overview
    2. Main Contributions
    3. Methodology
    4. Results
    5. Conclusion

    Research Paper:
    {text[:12000]}
    """

    response = model.generate_content(prompt)

    return response.text