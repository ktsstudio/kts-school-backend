from aiohttp import web
from marshmallow_dataclass import dataclass

import asyncio
from typing import Optional

import aiomongo
from aiomongo import Database, Collection


@dataclass
class MongoConfigRequired:
    db: str


@dataclass
class MongoConfigOptional:
    host: str = "127.0.0.1"
    port: int = 27017
    username: Optional[str] = None
    password: Optional[str] = None
    auth_db: Optional[str] = None
    maxpoolsize: int = 1
    reconnect_timeout: float = 1.0


@dataclass
class MongoConfig(MongoConfigOptional, MongoConfigRequired):
    pass


class AioMongoAccessor:
    def __init__(self):
        self._conn = None
        self.config: Optional[MongoConfig] = None

    def setup(self, application: web.Application) -> None:
        application.on_startup.append(self._connect)
        application.on_cleanup.append(self._disconnect)

    async def _connect(self, application: web.Application) -> None:
        self.config = MongoConfig.Schema().load(application["config"]["mongo"])

        while True:
            try:
                self._conn = await aiomongo.create_client(
                    self._build_connection_string(),
                )
                await self.ping()
                application["store"] = {"db": self}
                return
            except Exception as e:
                print(
                    "Cannot connect to mongo (%s:%d/%s): %s",
                    self.config.host,
                    self.config.port,
                    self.config.db,
                    str(e),
                )
                await asyncio.sleep(self.config.reconnect_timeout)

    async def _disconnect(self, *args, **kwargs) -> None:
        if self.conn is not None:
            self.conn.close()
            self._conn = None

    @property
    def conn(self) -> aiomongo.AioMongoClient:
        return self._conn

    @property
    def db(self) -> Database:
        return self.conn[self.config.db] if self.conn else None

    def get_db(self, db) -> Database:
        return self.conn[db] if self.conn else None

    def collection(self, collection_name: str) -> Collection:
        return getattr(self.db, collection_name)

    async def ping(self) -> bool:
        # noinspection PyBroadException
        try:
            await self.get_db("admin").command({"ping": 1})
            return True
        except Exception:
            return False

    def _build_connection_string(self) -> str:
        hosts = f"{self.config.host}:{self.config.port}"

        if self.config.username and self.config.password:
            hosts = f"{self.config.username}:{self.config.password}@{hosts}"

        q = [f"maxpoolsize={self.config.maxpoolsize}"]

        if self.config.auth_db:
            q.append(f"authSource={self.config.auth_db}")

        q = "&".join(q)

        return f"mongodb://{hosts}/{self.config.db}?{q}"
