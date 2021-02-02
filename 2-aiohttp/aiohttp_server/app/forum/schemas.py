import datetime

from marshmallow import Schema, fields

from app.base.schemas import BaseResponseSchema


class Message(Schema):
    id = fields.Integer()
    text = fields.String()
    created = fields.DateTime()
    polarity = fields.Float()
    subjectivity = fields.Float()


class CreateMessageRequestSchema(Schema):
    text = fields.String(required=True)


class CreateMessageResponseSchema(Schema):
    id: int = fields.Int()
    text: str = fields.Str()
    created: datetime.datetime = fields.DateTime()
    polarity: float = fields.Float()
    subjectivity: float = fields.Float()


class ListMessageResponseSchema(BaseResponseSchema):
    messages = fields.Nested(Message, many=True)
