import datetime
from dataclasses import field
from typing import List, Optional

from app.base.schemas import BaseDataclassSchema
from marshmallow_dataclass import dataclass


@dataclass
class GetListRequest(BaseDataclassSchema):
    limit: Optional[int] = field(metadata={"required": False}, default=None)
    offset: Optional[int] = field(metadata={"required": False}, default=None)


@dataclass
class GetAirportRequest(BaseDataclassSchema):
    airport_code: str


@dataclass
class GetFlightRequest(BaseDataclassSchema):
    flight_id: int


@dataclass
class AirportDC(BaseDataclassSchema):
    airport_code: str
    airport_name: str
    city: str
    longitude: float
    latitude: float
    timezone: str


@dataclass
class FlightDC(BaseDataclassSchema):
    flight_id: int
    flight_no: str
    scheduled_departure: datetime.datetime
    scheduled_arrival: datetime.datetime
    departure_airport: str
    arrival_airport: str
    status: str
    aircraft_code: str
    actual_departure: Optional[datetime.datetime]
    actual_arrival: Optional[datetime.datetime]

    departure_airport_info: Optional[AirportDC] = field(
        metadata={"required": True}, default=None
    )
    arrival_airport_info: Optional[AirportDC] = field(
        metadata={"required": True}, default=None
    )


@dataclass
class AirportListDC(BaseDataclassSchema):
    airports: List[AirportDC] = field(metadata={"required": True}, default_factory=list)


@dataclass
class StatItem(BaseDataclassSchema):
    passenger_id: str
    times: int
    amount: int


@dataclass
class Stat(BaseDataclassSchema):
    passengers: List[StatItem] = field(
        metadata={"required": True}, default_factory=list
    )
