import csv
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

from medintel.ingestion.models import IngestionError, IngestionResult
from medintel.models.presentation import Presentation

EXPECTED_FIELD_COUNT = 13
DATE_FORMAT = "%d/%m/%Y"


def parse_date(value: str) -> date | None:
    value = value.strip()

    if not value:
        return None

    return datetime.strptime(value, DATE_FORMAT).date()


def parse_decimal(value: str) -> Decimal | None:
    value = value.strip().replace(",", ".")

    if not value:
        return None

    try:
        return Decimal(value)
    except InvalidOperation:
        return None


def parse_presentation_row(row: list[str]) -> Presentation:
    if len(row) != EXPECTED_FIELD_COUNT:
        raise ValueError(
            f"Expected {EXPECTED_FIELD_COUNT} fields, got {len(row)}"
        )

    return Presentation(
        cis=row[0].strip(),
        cip7=row[1].strip(),
        name=row[2].strip(),
        administrative_status=row[3].strip(),
        commercialization_status=row[4].strip(),
        commercialization_date=parse_date(row[5]),
        cip13=row[6].strip(),
        collective_agreement=row[7].strip(),
        reimbursement_rate=row[8].strip(),
        price=parse_decimal(row[9]),
        public_price=parse_decimal(row[10]),
        dispensing_fee=parse_decimal(row[11]),
        reimbursement_indications=row[12].strip(),
    )


def parse_bdpm_presentation_file(file_path: Path) -> IngestionResult:
    presentations: list[Presentation] = []
    errors: list[IngestionError] = []

    with file_path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:
        reader = csv.reader(file, delimiter="\t")

        for row_number, row in enumerate(reader, start=1):
            try:
                presentations.append(parse_presentation_row(row))
            except (ValueError, TypeError) as error:
                errors.append(
                    IngestionError(
                        row_number=row_number,
                        error=str(error),
                    )
                )

    return IngestionResult(
        items=presentations,
        total_rows=len(presentations) + len(errors),
        successful_rows=len(presentations),
        failed_rows=len(errors),
        errors=errors,
    )