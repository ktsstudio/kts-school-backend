from app.store.database.models import db


class Airport(db.Model):
    airport_code = db.Column(db.BigInteger(), primary_key=True)
    airport_name = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    longitude = db.Column(db.Float(), nullable=False)
    latitude = db.Column(db.db.Float()(), nullable=False)
    timezone = db.Column(db.String(50), nullable=False)
