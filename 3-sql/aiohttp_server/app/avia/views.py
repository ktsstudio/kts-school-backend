from typing import Optional, List

import aiohttp_jinja2
from aiohttp import web
from aiohttp.web_exceptions import HTTPNotFound
from aiohttp_apispec import docs, response_schema, querystring_schema
from gino.loader import ColumnLoader

from app.avia.models import Airport, Flight, TicketFlight, Ticket
from app.avia.schemas import (
    AirportDC,
    AirportListDC,
    GetAirportRequest,
    GetFlightRequest,
    FlightDC,
    GetListRequest,
    Stat,
    StatItem,
)
from app.base.responses import json_response
from app.store.database.models import db


@aiohttp_jinja2.template("index.html")
async def index(_):
    return {}


class AirportListView(web.View):
    @docs(tags=["airport"],)
    @querystring_schema(GetListRequest.Schema())
    @response_schema(AirportListDC.Schema(), 200)
    async def get(self):
        query = self.request.query
        limit: str = query.get("limit", 100)
        offset: str = query.get("offset", 0)
        airports_plenty = await Airport.query.limit(limit).offset(offset).gino.all()
        return json_response(
            data=AirportListDC.Schema().dump(
                AirportListDC(airports=[a.to_dc() for a in airports_plenty])
            )
        )


class GetAirportView(web.View):
    @docs(tags=["airport"],)
    @querystring_schema(GetAirportRequest.Schema())
    @response_schema(AirportDC.Schema(), 200)
    async def get(self):
        query = self.request.query
        airport_code: str = query.get("airport_code")

        airport: Optional[Airport] = (
            await Airport.query.where(Airport.airport_code == airport_code,)
            .gino.load(Airport)
            .first()
        )
        if airport is None:
            raise HTTPNotFound

        return json_response(data=AirportDC.Schema().dump(airport.to_dc()))


class GetFlightView(web.View):
    @docs(tags=["flight"],)
    @querystring_schema(GetFlightRequest.Schema())
    @response_schema(FlightDC.Schema(), 200)
    async def get(self):
        flight_id: int = int(self.request.query.get("flight_id"))

        airport_from: Airport = Airport.alias("airport_from")
        airport_to: Airport = Airport.alias("airport_to")
        flight: Optional[Flight] = (
            await Flight.outerjoin(
                airport_from, airport_from.airport_code == Flight.departure_airport
            )
            .outerjoin(airport_to, airport_to.airport_code == Flight.arrival_airport)
            .select()
            .where(Flight.flight_id == flight_id)
            .gino.load(
                # Flight
                Flight.load(
                    departure_airport_info=airport_from, arrival_airport_info=airport_to
                )
            )
            .all()
        )
        if not flight:
            raise HTTPNotFound

        return json_response(data=FlightDC.Schema().dump(flight[0].to_dc()))


class MoneySpendView(web.View):
    @docs(tags=["passenger"],)
    @response_schema(Stat.Schema(), 200)
    async def get(self):
        times_func = db.func.count(Ticket.passenger_id)
        amount_func = db.func.sum(TicketFlight.amount)

        query = (
            db.select([Ticket.passenger_id, times_func, amount_func])
            .select_from(
                Ticket.outerjoin(
                    TicketFlight, Ticket.ticket_no == TicketFlight.ticket_no
                )
            )
            .group_by(Ticket.passenger_id)
            .gino.load(
                (
                    Ticket.passenger_id,
                    ColumnLoader(times_func),
                    ColumnLoader(amount_func),
                )
            )
        )

        res = Stat()
        async with db.transaction():
            async for passenger_id, times, amount in query.iterate():
                res.passengers.append(
                    StatItem(passenger_id=passenger_id, times=times, amount=amount)
                )



        return json_response(data=Stat.Schema().dump(res))
