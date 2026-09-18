from medintel.config import settings
from medintel.ingestion.bdpm_presentation_parser import parse_bdpm_presentation_file
from medintel.structured.presentation_repository import PresentationRepository


def load_presentation_repository() -> PresentationRepository:
    result = parse_bdpm_presentation_file(
        settings.data_raw_path / "CIS_CIP_bdpm.txt"
    )

    return PresentationRepository(
        presentations=result.items,
    )