import aiohttp_jinja2
from aiohttp import web
from app.rnb import views


@aiohttp_jinja2.template("index.html")
async def index(_):
    return {}


def setup_routes(app: web.Application) -> None:
    app.router.add_get("/", index)
    app.router.add_view("/api/accomodation.list", views.AccomodationListView)
    app.router.add_view("/api/accomodation.get", views.GetAccomodationView)
    app.router.add_view("/api/accomodation.get_stat", views.StrangeStat)
