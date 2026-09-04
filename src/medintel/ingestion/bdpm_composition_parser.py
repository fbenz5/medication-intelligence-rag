import csv
from pathlib import Path

from medintel.ingestion.models import IngestionError, IngestionResult
from medintel.models.composition import Composition

EXPECTED_FIELD_COUNT = 8


def parse_composition_row(row: list[str]) -> Composition:
    if len(row) != EXPECTED_FIELD_COUNT:
        raise ValueError(
            f"Expected {EXPECTED_FIELD_COUNT} fields, got {len(row)}"
        )

    return Composition(
        cis=row[0].strip(),
        pharmaceutical_element=row[1].strip(),
        substance_code=row[2].strip(),
        substance_name=row[3].strip(),
        dosage=row[4].strip(),
        dosage_reference=row[5].strip(),
        component_type=row[6].strip(),
        component_link_number=row[7].strip(),
    )


def parse_bdpm_composition_file(file_path: Path) -> IngestionResult:
    compositions: list[Composition] = []
    errors: list[IngestionError] = []

    with file_path.open(
        "r",
        encoding="cp1250",
        newline="",
    ) as file:
        reader = csv.reader(file, delimiter="\t")

        for row_number, row in enumerate(reader, start=1):
            try:
                compositions.append(parse_composition_row(row))
            except (ValueError, TypeError):
                errors.append(
                    IngestionError(
                        row_number=row_number,
                        error="Invalid composition row",
                    )
                )

    return IngestionResult(
        items=compositions,
        total_rows=len(compositions) + len(errors),
        successful_rows=len(compositions),
        failed_rows=len(errors),
        errors=errors,
    )