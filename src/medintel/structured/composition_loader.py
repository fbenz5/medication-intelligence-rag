from pathlib import Path

from medintel.ingestion.bdpm_composition_parser import (
    parse_bdpm_composition_file,
)
from medintel.structured.composition_repository import CompositionRepository

RAW_DATA_PATH = Path("data/raw")


def load_composition_repository() -> CompositionRepository:
    result = parse_bdpm_composition_file(
        RAW_DATA_PATH / "CIS_COMPO_bdpm.txt"
    )

    return CompositionRepository(
        compositions=result.items,
    )