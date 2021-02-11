from typing import Optional, List

import aiohttp_jinja2
from aiohttp import web
from aiohttp.web_exceptions import HTTPNotFound
from aiohttp_apispec import docs, response_schema, querystring_schema

from app.rnb.schemas import (
    AccomodationList,
    BaseAccomodation,
    Accomodation,
    GetByIdRequest,
    StatItem,
    Stat,
)
from app.base.responses import json_response
from app.store.database.accessor import AioMongoAccessor


@aiohttp_jinja2.template("index.html")
async def index(_):
    return {}


class AccomodationListView(web.View):
    @docs(tags=["accomodation"],)
    @response_schema(AccomodationList.Schema(), 200)
    async def get(self):
        query = self.request.query
        limit: str = query.get("limit", 100)
        offset: str = query.get("offset", 0)

        store: AioMongoAccessor = self.request.app.get("store").get("db")
        accomodations = (
            await store.collection("accomodation").find().limit(10).to_list()
        )

        return json_response(
            data={
                "accomodations": BaseAccomodation.Schema().dump(
                    BaseAccomodation.Schema().load(accomodations, many=True), many=True
                )
            }
        )


class GetAccomodationView(web.View):
    @docs(tags=["accomodation"],)
    @querystring_schema(GetByIdRequest.Schema())
    @response_schema(Accomodation.Schema(), 200)
    async def get(self):
        query = self.request.query
        accomodation_id: int = int(query.get("id"))

        store: AioMongoAccessor = self.request.app.get("store").get("db")
        cur = await store.collection("accomodation").aggregate(
            [
                {"$match": {"id": accomodation_id}},
                {
                    "$lookup": {
                        "from": "review",
                        "localField": "id",
                        "foreignField": "listing_id",
                        "as": "reviews",
                    }
                },
            ]
        )

        accomodation: Optional[Accomodation] = None
        async for d in cur:
            accomodation = Accomodation.Schema().load(d)
            break

        if accomodation is None:
            raise HTTPNotFound

        return json_response(data=Accomodation.Schema().dump(accomodation))


class StrangeStat(web.View):
    @docs(tags=["accomodation"],)
    @querystring_schema(GetByIdRequest.Schema())
    @response_schema(Stat.Schema(), 200)
    async def get(self):
        query = self.request.query
        accomodation_id: int = int(query.get("id"))

        store: AioMongoAccessor = self.request.app.get("store").get("db")
        cur = await store.collection("accomodation").aggregate(
            [
                {"$match": {"id": accomodation_id}},
                {
                    "$lookup": {
                        "from": "review",
                        "localField": "id",
                        "foreignField": "listing_id",
                        "as": "reviews",
                    }
                },
                {
                    "$lookup": {
                        "from": "review",
                        "localField": "id",
                        "foreignField": "listing_id",
                        "as": "reviews",
                    }
                },
                {"$unwind": "$reviews"},
                {"$addFields": {"review_date": {"$toDate": "$reviews.date"},}},
                {
                    "$group": {
                        "_id": "$reviews.reviewer_id",
                        "times": {"$sum": 1},
                        "first_date": {"$min": "$review_date"},
                        "last_date": {"$max": "$review_date"},
                        "comments": {"$addToSet": "$reviews.comments"},
                    }
                },
                {"$match": {"times": {"$gt": 1}}},
            ]
        )

        cases: List[StatItem] = list()
        async for d in cur:
            item = StatItem.Schema().load(
                {
                    **d,
                    "first_date": d.get("first_date").isoformat(),
                    "last_date": d.get("last_date").isoformat(),
                }
            )
            cases.append(item)

        return json_response(data={"cases": StatItem.Schema().dump(cases, many=True)})
