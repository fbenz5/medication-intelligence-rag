import csv
from pathlib import Path

FILE_PATH = Path("data/raw/CIS_bdpm.txt")


def main() -> None:
    with FILE_PATH.open("r", encoding="cp1252", newline="") as file:
        reader = csv.reader(file, delimiter="\t")

        for row_number, row in enumerate(reader):
            print(f"Row {row_number + 1}:")
            print(f"  Number of fields: {len(row)}")
            print(f"  Fields: {row}")

            if row_number == 4:
                break


if __name__ == "__main__":
    main()