from datetime import date

from pydantic import BaseModel


class Medication(BaseModel):
    cis: str
    name: str
    pharmaceutical_form: str
    administration_routes: str
    administrative_status: str
    authorization_procedure: str
    commercialization_status: str
    authorization_date: date | None
    bdm_status: str
    european_authorization_number: str
    marketing_authorization_holder: str
    enhanced_monitoring: str