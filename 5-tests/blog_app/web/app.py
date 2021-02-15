from aiohttp import web
from aiohttp_apispec import setup_aiohttp_apispec, validation_middleware

from blog_app.web.middlewares import auth_middleware, error_middleware
from blog_app.store.store import Store
from blog_app.web.urls import setup_routes


def create_app():
    app = web.Application(
        middlewares=[error_middleware, auth_middleware, validation_middleware]
    )
    setup_routes(app)
    app["store"] = Store(app)
    setup_aiohttp_apispec(
        app=app,
        title="My Documentation",
        version="v1",
        url="/api/docs/swagger.json",
        swagger_path="/api/docs",
    )
    return app
