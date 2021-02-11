import datetime
from dataclasses import field
from typing import List

from app.base.schemas import BaseDataclassSchema
from marshmallow_dataclass import dataclass


@dataclass
class Id(BaseDataclassSchema):
    id: int


@dataclass
class GetByIdRequest(Id):
    pass


@dataclass
class BaseAccomodation(Id):
    listing_url: str
    last_scraped: str
    name: str
    description: str
    neighborhood_overview: str
    picture_url: str


@dataclass
class Review(BaseDataclassSchema):
    id: int
    listing_id: int
    date: datetime.date
    reviewer_id: int
    reviewer_name: str
    comments: str


@dataclass
class Accomodation(BaseAccomodation):
    reviews: List[Review]


@dataclass
class AccomodationList(BaseDataclassSchema):
    accomodations: List[BaseAccomodation] = field(
        metadata={"required": True}, default_factory=list
    )


@dataclass
class StatItem(BaseDataclassSchema):
    times: int
    first_date: datetime.datetime
    last_date: datetime.datetime
    comments: List[str] = field(metadata={"required": True}, default_factory=list)


@dataclass
class Stat(BaseAccomodation):
    cases: List[StatItem] = field(metadata={"required": True}, default_factory=list)
