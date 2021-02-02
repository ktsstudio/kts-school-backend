import ssl

from aiohttp import web
from sqlalchemy import func


class PostgresAccessor:
    def __init__(self) -> None:
        from app.forum.models import Message

        self.message = Message
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

    async def get_total_polarity_and_subjectivity(self):
        average_polarity = await self.db.func.avg(self.message.polarity).gino.scalar()
        average_subjectivity = await self.db.func.avg(
            self.message.subjectivity
        ).gino.scalar()
        return average_polarity, average_subjectivity
