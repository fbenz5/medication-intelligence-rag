from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class Presentation(BaseModel):
    cis: str
    cip7: str
    name: str
    administrative_status: str
    commercialization_status: str
    commercialization_date: date | None
    cip13: str
    collective_agreement: str
    reimbursement_rate: str
    price: Decimal | None
    public_price: Decimal | None
    dispensing_fee: Decimal | None
    reimbursement_indications: str