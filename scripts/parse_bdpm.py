from pathlib import Path

from medintel.ingestion.bdpm_parser import parse_bdpm_file

FILE_PATH = Path("data/raw/CIS_bdpm.txt")


def main() -> None:
    medications = parse_bdpm_file(FILE_PATH)

    print(f"Parsed medications: {len(medications)}")

    print("\nFirst 5 medications:")
    for medication in medications[:5]:
        print(medication)


if __name__ == "__main__":
    main()