import ssl

from aiohttp import web


class PostgresAccessor:
    def __init__(self) -> None:
        self.db = None

    def setup(self, application: web.Application) -> None:
        application.on_startup.append(self._on_connect)
        application.on_cleanup.append(self._on_disconnect)

    async def _on_connect(self, application: web.Application):
        from app.store.database.models import db

        self.config = application["config"]["postgres"]
        if self.config["require_ssl"]:
            ctx = ssl.create_default_context(cafile="")
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            await db.set_bind(self.config["database_url"], ssl=ctx)
        else:
            await db.set_bind(self.config["database_url"])
        self.db = db
        application["db"] = self

    async def _on_disconnect(self, _) -> None:
        if self.db is not None:
            await self.db.pop_bind().close()
