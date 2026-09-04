import re


def clean_text(text: str) -> str:
    # Repair words split by a hyphen at a line break.
    text = re.sub(r"-\s*\n\s*", "", text)

    # Remove isolated PDF bullet/layout characters.
    text = re.sub(r"^\s*‒\s*$", "", text, flags=re.MULTILINE)

    # Remove the repeated HAS page header and page number.
    text = re.sub(
        r"^HAS • Médicaments antiémétiques dans le traitement symptomatique "
        r"des nausées et des vomissements • novembre 2022\s*$",
        "",
        text,
        flags=re.MULTILINE,
    )

    # Remove isolated page numbers.
    text = re.sub(r"^\s*\d+\s*$", "", text, flags=re.MULTILINE)

    # Remove the incomplete "Mis à jour en" PDF artifact.
    text = re.sub(r"^Mis à jour en\s*$", "", text, flags=re.MULTILINE)

    # Remove spaces immediately after a hyphen.
    text = re.sub(r"-\s+", "-", text)

    # Normalize spaces within lines.
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines.
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()