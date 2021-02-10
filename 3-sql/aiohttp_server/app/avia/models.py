from sqlalchemy.dialects.postgresql import JSONB

from app.store.database.models import db

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.avia.schemas import AirportDC, FlightDC


class DCConverter:
    def to_dc(self):
        raise NotImplementedError


class Airport(db.Model, DCConverter):
    __tablename__ = "airports"

    airport_code = db.Column(db.String(3), primary_key=True)
    airport_name = db.Column(db.Text(), nullable=False)
    city = db.Column(db.Text(), nullable=False)
    longitude = db.Column(db.Float(), nullable=False)
    latitude = db.Column(db.Float(), nullable=False)
    timezone = db.Column(db.Text(), nullable=False)

    def to_dc(self) -> "AirportDC":
        from app.avia.schemas import AirportDC

        a = 5

        return AirportDC.Schema().load(self.__values__)


class Flight(db.Model, DCConverter):
    __tablename__ = "flights"

    flight_id = db.Column(db.Integer(), primary_key=True)
    flight_no = db.Column(db.String(6), nullable=False)
    scheduled_departure = db.Column(db.DateTime(timezone=True), nullable=False)
    scheduled_arrival = db.Column(db.DateTime(timezone=True), nullable=False)
    departure_airport = db.Column(
        db.String(3), db.ForeignKey("airports.airport_code"), nullable=False
    )
    arrival_airport = db.Column(
        db.String(3), db.ForeignKey("airports.airport_code"), nullable=False
    )
    status = db.Column(db.String(20), nullable=False)
    aircraft_code = db.Column(db.String(3), nullable=False)
    actual_departure = db.Column(db.DateTime(timezone=True), nullable=True)
    actual_arrival = db.Column(db.DateTime(timezone=True), nullable=True)

    def __init__(self, **kw):
        super().__init__(**kw)
        self._departure_airport_info: Optional[Airport] = None
        self._arrival_airport_info: Optional[Airport] = None

    def to_dc(self) -> "FlightDC":
        from app.avia.schemas import FlightDC

        flight = FlightDC.Schema().load(
            {
                **self.__values__,
                "scheduled_departure": self.scheduled_departure.isoformat(),
                "scheduled_arrival": self.scheduled_arrival.isoformat(),
                "actual_departure": None
                if self.scheduled_arrival is None
                else self.actual_departure.isoformat(),
                "actual_arrival": None
                if self.actual_arrival is None
                else self.actual_arrival.isoformat(),
                "departure_airport_info": None
                if self._departure_airport_info is None
                else self._departure_airport_info.__values__,
                "arrival_airport_info": None
                if self._arrival_airport_info is None
                else self._arrival_airport_info.__values__,
            }
        )
        return flight

    @property
    def departure_airport_info(self) -> Optional[Airport]:
        return self

    @departure_airport_info.setter
    def departure_airport_info(self, airport: Optional[Airport]):
        self._departure_airport_info = airport

    @property
    def arrival_airport_info(self) -> Optional[Airport]:
        return self

    @arrival_airport_info.setter
    def arrival_airport_info(self, airport: Optional[Airport]):
        self._arrival_airport_info = airport


class Ticket(db.Model, DCConverter):
    __tablename__ = "tickets"

    ticket_no = db.Column(db.String(13), primary_key=True)
    book_ref = db.Column(db.String(6), nullable=False)
    passenger_id = db.Column(db.String(20), nullable=False, index=True)
    passenger_name = db.Column(db.Text(), nullable=False)
    contact_data = db.Column(JSONB)


class TicketFlight(db.Model, DCConverter):
    __tablename__ = "ticket_flights"

    ticket_no = db.Column(
        db.String(13), nullable=False
    )
    flight_id = db.Column(db.Integer(), nullable=False)
    fare_conditions = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Numeric(), nullable=False)
