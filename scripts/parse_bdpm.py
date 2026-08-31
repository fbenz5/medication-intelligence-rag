from pathlib import Path

from medintel.ingestion.bdpm_parser import parse_bdpm_file


FILE_PATH = Path("data/raw/CIS_bdpm.txt")


def main() -> None:
    result = parse_bdpm_file(FILE_PATH)

    print(f"Total rows: {result.total_rows}")
    print(f"Successfully parsed: {result.successful_rows}")
    print(f"Failed: {result.failed_rows}")

    if result.errors:
        print("\nFirst 5 errors:")
        for error in result.errors[:5]:
            print(f"  Row {error.row_number}: {error.error}")

    print("\nFirst 5 medications:")
    for medication in result.medications[:5]:
        print(medication)


if __name__ == "__main__":
    main()