import re


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.compile(r"\s+").sub("-", text)
    text = re.compile(r"([^A-Za-z0-9-])+").sub("-", text)
    text = re.compile(r"--+").sub("-", text)
    text = re.compile(r"(^-|-$)").sub("", text)
    return text
