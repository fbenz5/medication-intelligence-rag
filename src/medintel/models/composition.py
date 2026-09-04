from pydantic import BaseModel


class Composition(BaseModel):
    cis: str
    pharmaceutical_element: str
    substance_code: str
    substance_name: str
    dosage: str
    dosage_reference: str
    component_type: str
    component_link_number: str