def quiz_prompt(text, num_questions=5):
    return f"""
Create {num_questions} multiple-choice questions from the research paper.

Format EXACTLY like this:

Q1. Question text

A) Option A
B) Option B
C) Option C
D) Option D

Answer: B

Explanation: Explanation text


Q2. Question text

A) Option A
B) Option B
C) Option C
D) Option D

Answer: A

Explanation: Explanation text

Research Paper:
{text[:8000]}
"""