import functools

from aiohttp.web_exceptions import HTTPUnauthorized


def require_auth(func):
    @functools.wraps(func)
    async def require_auth_wrap(self, *args, **kwargs):
        if "user_id" not in self.request:
            raise HTTPUnauthorized
        return await func(self, *args, **kwargs)

    return require_auth_wrap
