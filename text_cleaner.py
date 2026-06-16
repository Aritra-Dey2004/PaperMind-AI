import re

def clean_text_func(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()