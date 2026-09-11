from medintel.structured.loader import load_medication_repository

CIS = "60002283"


def main() -> None:
    repository = load_medication_repository()

    medication = repository.get_medication(CIS)

    if medication is None:
        print(f"Medication {CIS} not found.")
        return

    print("Medication found:")
    print(f"CIS: {medication.cis}")
    print(f"Name: {medication.name}")
    print(f"Pharmaceutical form: {medication.pharmaceutical_form}")
    print(f"Administrative status: {medication.administrative_status}")
    print(f"Commercialization status: {medication.commercialization_status}")

    medications = repository.search_by_name("domperidone")

    print(f"\nName search results: {len(medications)}")

    for medication in medications[:5]:
        print(f"{medication.cis} - {medication.name}")


if __name__ == "__main__":
    main()