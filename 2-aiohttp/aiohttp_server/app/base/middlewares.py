from aiohttp import web

from app.base.responses import json_response


@web.middleware
async def error_middleware(request, handler):
    try:
        return await handler(request)
    except web.HTTPException as ex:
        return json_response(status=ex.status, text_status=ex.text, data={})
    except Exception as e:
        return json_response(status=500, text_status=str(e), data={})
