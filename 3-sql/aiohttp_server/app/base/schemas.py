from typing import ClassVar, Type

from marshmallow import Schema, EXCLUDE, fields
from marshmallow_dataclass import dataclass

from marshmallow import Schema, fields


class BaseResponseSchema(Schema):
    status = fields.Str()
    data = fields.Dict(allow_none=None)


class BaseDataclassSchema:
    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


@dataclass
class BaseResponse(BaseDataclassSchema):
    status: str
    data: dict = fields.Dict(allow_none=None)
