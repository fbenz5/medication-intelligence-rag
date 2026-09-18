from medintel.config import settings
from medintel.ingestion.bdpm_parser import parse_bdpm_file
from medintel.structured.repository import MedicationRepository


def load_medication_repository() -> MedicationRepository:
    result = parse_bdpm_file(
        settings.data_raw_path / "CIS_bdpm.txt"
    )

    return MedicationRepository(
        medications=result.items,
    )