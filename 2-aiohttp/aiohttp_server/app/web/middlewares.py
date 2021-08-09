import json
import typing

from aiohttp_apispec.middlewares import validation_middleware
from aiohttp.web import middleware
from aiohttp.web_exceptions import HTTPException, HTTPUnprocessableEntity

from app.web.utils import error_json_response

if typing.TYPE_CHECKING:
    from app.web.app import Application


@middleware
async def error_handling_middleware(request, handler):
    try:
        response = await handler(request)
        return response
    except HTTPUnprocessableEntity as e:
        return error_json_response(http_status=400, status='bad request', message=e.reason, data=json.loads(e.text))
    except HTTPException as e:
        return error_json_response(http_status=e.status, status='error', message=str(e))
    except Exception as e:
        return error_json_response(http_status=500, status='internal server error', message=str(e))


def setup_middlewares(app: "Application"):
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(validation_middleware)
