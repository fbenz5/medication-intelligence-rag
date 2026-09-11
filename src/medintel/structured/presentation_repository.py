from medintel.models.presentation import Presentation


class PresentationRepository:
    def __init__(self, presentations: list[Presentation]) -> None:
        self._presentations_by_cis: dict[str, list[Presentation]] = {}

        for presentation in presentations:
            self._presentations_by_cis.setdefault(
                presentation.cis,
                [],
            ).append(presentation)

    def get_by_cis(self, cis: str) -> list[Presentation]:
        return self._presentations_by_cis.get(cis, [])

    def get_all_presentations(self) -> list[Presentation]:
        return [
            presentation
            for presentations in self._presentations_by_cis.values()
            for presentation in presentations
        ]