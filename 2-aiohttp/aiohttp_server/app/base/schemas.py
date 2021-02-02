from marshmallow import Schema, fields


class BaseResponseSchema(Schema):
    status = fields.Str()
    data = fields.Dict(allow_none=None)
