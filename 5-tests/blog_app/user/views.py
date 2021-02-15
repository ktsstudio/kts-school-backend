import datetime
from hashlib import md5
from uuid import uuid4

import aiohttp
from aiohttp import web
from aiohttp.web_exceptions import HTTPBadRequest
from aiohttp_apispec import docs, json_schema, response_schema
from asyncpg import UniqueViolationError
from sqlalchemy import and_

from blog_app.user.models import User, Session
from blog_app.user.schemas import RegisterSchema, LoginSchema, UserSchema
from blog_app.web.decorators import require_auth


class RegisterView(web.View):
    @docs(tags=["user"], summary="User registration")
    @json_schema(RegisterSchema)
    @response_schema(RegisterSchema)
    async def post(self):
        try:
            password_hash = md5(
                self.request["json"]["password"].encode()
            ).hexdigest()
            user = await User.create(
                username=self.request["json"]["username"],
                password=password_hash,
                created=datetime.datetime.utcnow(),
            )
        except UniqueViolationError:
            raise HTTPBadRequest(reason="user_already_exists")
        return web.json_response(UserSchema().dump(user))


class LoginView(web.View):
    @docs(tags=["user"], summary="User login")
    @json_schema(RegisterSchema)
    @response_schema(LoginSchema)
    async def post(self):
        user = await User.query.where(
            and_(
                User.username == self.request["json"]["username"],
                User.password
                == md5(self.request["json"]["password"].encode()).hexdigest(),
            )
        ).gino.first()

        if user:
            session = await Session.generate(user.id)
            return web.json_response({"token": session.key})
        raise HTTPBadRequest(reason="invalid_credentials")


class MeView(web.View):
    @docs(tags=["user"], summary="Information about current user")
    @response_schema(UserSchema)
    @require_auth
    async def get(self):
        user = await User.get(self.request["user_id"])
        return web.json_response(UserSchema().dump(user))


class ExternalView(web.View):
    @docs(tags=["user"], summary="View with external requests")
    async def get(self):
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                "https://www.metaweather.com/api/location/44418/"
            )
            return web.json_response(await response.json())
