from medintel.ingestion.document_cleaner import clean_text


def test_clean_text_repairs_hyphenated_line_breaks() -> None:
    text = "métoclo-\npramide"

    result = clean_text(text)

    assert result == "métoclopramide"


def test_clean_text_removes_isolated_bullet_characters() -> None:
    text = "First paragraph\n‒\nSecond paragraph"

    result = clean_text(text)

    assert result == "First paragraph\n\nSecond paragraph"


def test_clean_text_normalizes_excessive_whitespace() -> None:
    text = "First   paragraph\n\n\n\nSecond paragraph"

    result = clean_text(text)

    assert result == "First paragraph\n\nSecond paragraph"