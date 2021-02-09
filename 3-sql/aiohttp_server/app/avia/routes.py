import aiohttp_jinja2
from aiohttp import web
from app.avia import views


@aiohttp_jinja2.template("index.html")
async def index(_):
    return {}


def setup_routes(app: web.Application) -> None:
    app.router.add_get("/", index)
    app.router.add_view("/api/airport.list", views.AirportListView)
    app.router.add_view("/api/airport.get", views.GetAirportView)

    app.router.add_view("/api/flight.get", views.GetFlightView)

    app.router.add_view("/api/passenger.stat", views.MoneySpendView)
