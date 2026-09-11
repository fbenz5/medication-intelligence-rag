from pathlib import Path

from medintel.ingestion.bdpm_presentation_parser import parse_bdpm_presentation_file
from medintel.structured.presentation_repository import PresentationRepository

RAW_DATA_PATH = Path("data/raw")


def load_presentation_repository() -> PresentationRepository:
    result = parse_bdpm_presentation_file(
        RAW_DATA_PATH / "CIS_CIP_bdpm.txt"
    )

    return PresentationRepository(
        presentations=result.items,
    )