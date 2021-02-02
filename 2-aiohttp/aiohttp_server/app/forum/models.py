from app.store.database.models import db


class Message(db.Model):
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    polarity = db.Column(db.Float, nullable=False)
    subjectivity = db.Column(db.Float, nullable=False)
