from marshmallow import Schema, fields


class RegisterSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class LoginSchema(Schema):
    token = fields.Str(required=True)


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    created = fields.DateTime()
