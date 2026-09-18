from medintel.config import settings
from medintel.ingestion.bdpm_composition_parser import parse_bdpm_composition_file
from medintel.structured.composition_repository import CompositionRepository


def load_composition_repository() -> CompositionRepository:
    result = parse_bdpm_composition_file(
        settings.data_raw_path / "CIS_COMPO_bdpm.txt"
    )

    return CompositionRepository(
        compositions=result.items,
    )