from app.base.schemas import BaseDataclassSchema
from marshmallow_dataclass import dataclass


@dataclass
class AirportDC(BaseDataclassSchema):
    airport_code: str
    airport_name: str
    city: str
    longitude: float
    latitude: float
    timezone: str
