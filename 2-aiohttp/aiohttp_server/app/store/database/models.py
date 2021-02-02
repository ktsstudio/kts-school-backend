from gino import Gino

from app.store.database.accessor import PostgresAccessor

db = Gino()
# Все модели должны быть в памяти при миграциях,
# поэтому здесь инстанцируется аксессор, в котором они импортированы
database_accessor = PostgresAccessor()
