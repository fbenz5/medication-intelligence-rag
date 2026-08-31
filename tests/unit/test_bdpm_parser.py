from datetime import date

from medintel.ingestion.bdpm_parser import parse_medication_row


def test_parse_medication_row():
    row = [
        "63797011",
        "ABACAVIR SANDOZ 300 mg, comprimé pelliculé sécable",
        "comprimé pelliculé sécable",
        "orale",
        "Autorisation active",
        "Procédure décentralisée",
        "Commercialisée",
        "30/12/2016",
        "",
        "",
        "SANDOZ",
        "Non",
    ]

    medication = parse_medication_row(row)

    assert medication.cis == "63797011"
    assert medication.name == "ABACAVIR SANDOZ 300 mg, comprimé pelliculé sécable"
    assert medication.administration_routes == "orale"
    assert medication.authorization_date == date(2016, 12, 30)
    assert medication.european_authorization_number == ""
    assert medication.enhanced_monitoring == "Non"