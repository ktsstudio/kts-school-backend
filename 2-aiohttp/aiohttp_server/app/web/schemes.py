from marshmallow import Schema, fields


class OkResponseSchema(Schema):
    status = fields.Str()
    data = fields.Dict()
