from pathlib import Path

import pymupdf

FILE_PATH = Path("data/documents/has/bon_usage_antiemetiques.pdf")


def main() -> None:
    with pymupdf.open(FILE_PATH) as pdf:
        for page_number, page in enumerate(pdf, start=1):
            print(f"\n===== PAGE {page_number} =====\n")
            print(page.get_text("text"))


if __name__ == "__main__":
    main()