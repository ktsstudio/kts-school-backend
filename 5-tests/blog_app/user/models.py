import datetime
import uuid

from blog_app.store.database import db
from blog_app.utils import now


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.BigInteger(), primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(32), nullable=False)
    created = db.Column(db.DateTime(timezone=True), nullable=False)


class Session(db.Model):
    __tablename__ = "session"
    AGE_DAYS = 1

    key = db.Column(db.String(32), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)
    expires = db.Column(db.DateTime(timezone=True), nullable=False)
    created = db.Column(db.DateTime(timezone=True), nullable=False)

    @classmethod
    async def generate(cls, user_id):
        return await cls.create(
            user_id=user_id,
            key=uuid.uuid4().hex,
            created=now(),
            expires=now() + datetime.timedelta(days=cls.AGE_DAYS),
        )
