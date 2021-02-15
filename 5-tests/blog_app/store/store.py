from aiohttp import web
from sqlalchemy.engine.url import URL

from blog_app.store.database import db
from blog_app.settings import config


class Store:
    async def _db_connect(self, _app):
        await db.set_bind(
            URL(
                drivername="asyncpg",
                username=config["database"]["username"],
                password=config["database"]["password"],
                host=config["database"]["host"],
                port=config["database"]["port"],
                database=config["database"]["name"],
            ),
            min_size=1,
            max_size=1,
        )

    async def _db_disconnect(self, _app):
        await self.db.pop_bind().close()

    def __init__(self, app: web.Application):
        self.app = app
        self.db = db
        self.app.on_startup.append(self._db_connect)
        self.app.on_shutdown.append(self._db_disconnect)
