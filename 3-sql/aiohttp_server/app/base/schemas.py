from typing import ClassVar, Type

from marshmallow import Schema, EXCLUDE


class BaseDataclassSchema:
    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE
