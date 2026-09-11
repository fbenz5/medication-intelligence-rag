from medintel.models.composition import Composition


class CompositionRepository:
    def __init__(self, compositions: list[Composition]) -> None:
        self._compositions_by_cis: dict[str, list[Composition]] = {}

        for composition in compositions:
            self._compositions_by_cis.setdefault(
                composition.cis,
                [],
            ).append(composition)

    def get_by_cis(self, cis: str) -> list[Composition]:
        return self._compositions_by_cis.get(cis, [])

    def get_all_compositions(self) -> list[Composition]:
        return [
            composition
            for compositions in self._compositions_by_cis.values()
            for composition in compositions
        ]