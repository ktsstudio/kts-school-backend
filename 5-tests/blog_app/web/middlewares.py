import datetime

from aiohttp import web, hdrs
from sqlalchemy import and_

from blog_app.user.models import Session


def get_token(request: web.Request):
    authorization = request.headers.get(hdrs.AUTHORIZATION)
    if authorization:
        parts = authorization.split()
        if len(parts) == 2 and parts[0] == "Bearer":
            return parts[1]
    return None


@web.middleware
async def auth_middleware(request: web.Request, handler):
    token = get_token(request)
    if token:
        session = await Session.query.where(
            and_(
                Session.key == token,
                Session.expires >= datetime.datetime.utcnow(),
            )
        ).gino.first()
        if session:
            request["user_id"] = session.user_id
    return await handler(request)


@web.middleware
async def error_middleware(request, handler):
    try:
        return await handler(request)
    except web.HTTPException as ex:
        return web.json_response(
            status=ex.status, data={"code": ex.reason.lower()}
        )
    except Exception as e:
        request.app.logger.exception("Exception: {}".format(str(e)), exc_info=e)
        return web.json_response(status=500, data={"code": "internal_error"})
