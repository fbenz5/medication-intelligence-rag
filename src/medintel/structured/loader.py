from pathlib import Path

from medintel.ingestion.bdpm_parser import parse_bdpm_file
from medintel.structured.repository import MedicationRepository

RAW_DATA_PATH = Path("data/raw")


def load_medication_repository() -> MedicationRepository:
    result = parse_bdpm_file(
        RAW_DATA_PATH / "CIS_bdpm.txt"
    )

    return MedicationRepository(
        medications=result.items,
    )