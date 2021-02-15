from marshmallow import Schema, fields
from marshmallow.validate import Range

from blog_app.user.schemas import UserSchema


class CreatePostSchema(Schema):
    text = fields.Str(required=True)


class PostSchema(Schema):
    id = fields.Int()
    user = fields.Nested(UserSchema)
    text = fields.Str()
    created = fields.DateTime()


class PostListSchema(Schema):
    limit = fields.Int(missing=20, validate=Range(min=1, max=100))
    offset = fields.Int(missing=0, validate=Range(min=0))
    user_id = fields.Int()
