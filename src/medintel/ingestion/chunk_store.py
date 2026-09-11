import json
from pathlib import Path

from medintel.models.chunk import Chunk


def save_chunks(chunks: list[Chunk], file_path: Path) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding="utf-8") as file:
        for chunk in chunks:
            file.write(
                json.dumps(
                    chunk.model_dump(),
                    ensure_ascii=False,
                )
                + "\n"
            )


def load_chunks(file_path: Path) -> list[Chunk]:
    with file_path.open("r", encoding="utf-8") as file:
        return [
            Chunk.model_validate(json.loads(line))
            for line in file
            if line.strip()
        ]