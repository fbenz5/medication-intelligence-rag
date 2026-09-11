import re
import unicodedata


def normalize_text(text: str) -> str:
    text = text.lower()

    text = unicodedata.normalize("NFD", text)
    text = "".join(
        character
        for character in text
        if unicodedata.category(character) != "Mn"
    )

    text = re.sub(r"[^\w\s-]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()