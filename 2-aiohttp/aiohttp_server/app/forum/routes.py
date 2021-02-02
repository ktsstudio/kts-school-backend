from aiohttp import web

from app.forum.views import CreateMessageView, ListMessageView, index


def setup_routes(app: web.Application) -> None:
    app.router.add_get("/", index)
    app.router.add_view("/api/messages.create", CreateMessageView)
    app.router.add_view("/api/messages.list", ListMessageView)
