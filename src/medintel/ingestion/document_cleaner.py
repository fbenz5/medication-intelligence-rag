import re


def clean_text(text: str) -> str:
    # Repair words split by a hyphen at a line break.
    text = re.sub(r"-\s*\n\s*", "", text)

    # Remove isolated PDF bullet/layout characters.
    text = re.sub(r"^\s*‒\s*$", "", text, flags=re.MULTILINE)

    # Normalize spaces within lines.
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines.
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()