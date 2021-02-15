from aiohttp import web

from blog_app.web.app import create_app
from blog_app.settings import config

if __name__ == "__main__":
    web.run_app(create_app(), port=config["server"]["port"])
