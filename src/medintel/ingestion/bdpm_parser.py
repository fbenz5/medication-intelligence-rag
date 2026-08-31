import csv
from datetime import date, datetime
from pathlib import Path

from medintel.models.medication import Medication

EXPECTED_FIELD_COUNT = 12
DATE_FORMAT = "%d/%m/%Y"


def parse_authorization_date(value: str) -> date | None:
    value = value.strip()

    if not value:
        return None

    return datetime.strptime(value, DATE_FORMAT).date()


def parse_medication_row(row: list[str]) -> Medication:
    if len(row) != EXPECTED_FIELD_COUNT:
        raise ValueError(
            f"Expected {EXPECTED_FIELD_COUNT} fields, got {len(row)}"
        )

    return Medication(
        cis=row[0].strip(),
        name=row[1].strip(),
        pharmaceutical_form=row[2].strip(),
        administration_routes=row[3].strip(),
        administrative_status=row[4].strip(),
        authorization_procedure=row[5].strip(),
        commercialization_status=row[6].strip(),
        authorization_date=parse_authorization_date(row[7]),
        bdm_status=row[8].strip(),
        european_authorization_number=row[9].strip(),
        marketing_authorization_holder=row[10].strip(),
        enhanced_monitoring=row[11].strip(),
    )


def parse_bdpm_file(file_path: Path) -> list[Medication]:
    medications: list[Medication] = []

    with file_path.open(
        "r",
        encoding="cp1252",
        newline="",
    ) as file:
        reader = csv.reader(file, delimiter="\t")

        for row_number, row in enumerate(reader, start=1):
            try:
                medications.append(parse_medication_row(row))
            except (ValueError, TypeError) as error:
                raise ValueError(
                    f"Failed to parse BDPM row {row_number}: {error}"
                ) from error

    return medications