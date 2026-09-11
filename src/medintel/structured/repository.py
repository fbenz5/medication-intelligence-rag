from medintel.models.medication import Medication


class MedicationRepository:
    def __init__(self, medications: list[Medication]) -> None:
        self._medications = {
            medication.cis: medication
            for medication in medications
        }

    def get_medication(self, cis: str) -> Medication | None:
        return self._medications.get(cis)

    def search_by_name(self, name: str) -> list[Medication]:
        query = name.strip().lower()

        return [
            medication
            for medication in self._medications.values()
            if query in medication.name.lower()
        ]

    def get_all_medications(self) -> list[Medication]:
        return list(self._medications.values())