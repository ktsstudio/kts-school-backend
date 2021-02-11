import logging

import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp_apispec import setup_aiohttp_apispec, validation_middleware

from app.base.middlewares import error_middleware
from app.settings import config, BASE_DIR


def setup_config(application: web.Application) -> None:
    application["config"] = config


def setup_routes(application: web.Application) -> None:
    from app.rnb.routes import setup_routes as setup_rnb_routes

    setup_rnb_routes(application)

def setup_accessors(application: web.Application) -> None:
    from app.store.database.accessor import AioMongoAccessor

    database_accessor = AioMongoAccessor()
    database_accessor.setup(application)

def setup_middlewares(application: web.Application) -> None:
    application.middlewares.append(error_middleware)
    application.middlewares.append(validation_middleware)


def setup_external_libraries(application: web.Application) -> None:
    aiohttp_jinja2.setup(
        application, loader=jinja2.FileSystemLoader(f"{BASE_DIR}/templates")
    )
    setup_aiohttp_apispec(
        app=application,
        title="Forum documentation",
        version="v1",
        url="/swagger.json",
        swagger_path="/swagger",
    )


def setup_logging(application: web.Application) -> None:
    logging.basicConfig(level=logging.DEBUG)
    application.logger = logging.getLogger(__name__)


def setup_app(application: web.Application) -> None:
    setup_config(application)
    setup_routes(application)
    setup_accessors(application)
    setup_external_libraries(application)
    setup_middlewares(application)
    setup_logging(application)


app = web.Application()

if __name__ == "__main__":
    setup_app(app)
    web.run_app(app, port=config["common"]["port"])
