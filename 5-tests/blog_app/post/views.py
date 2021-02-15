import datetime

from aiohttp import web
from aiohttp_apispec import (
    docs,
    response_schema,
    json_schema,
    querystring_schema,
)
from sqlalchemy import and_

from blog_app.post.models import Post
from blog_app.post.schemas import CreatePostSchema, PostSchema, PostListSchema
from blog_app.user.models import User
from blog_app.web.decorators import require_auth


class CreatePostView(web.View):
    @docs(tags=["post"], summary="Create post")
    @json_schema(CreatePostSchema)
    @response_schema(PostSchema)
    @require_auth
    async def post(self):
        post = await Post.create(
            user_id=self.request["user_id"],
            text=self.request["json"]["text"],
            created=datetime.datetime.utcnow(),
        )
        return web.json_response(PostSchema().dump(post))


class PostListView(web.View):
    @docs(tags=["post"], summary="Post list")
    @querystring_schema(PostListSchema)
    @response_schema(PostSchema(many=True))
    async def get(self):
        data = self.request["querystring"]
        conditions = []
        if data.get("user_id"):
            conditions.append(Post.user_id == data["user_id"])

        posts = (
            await Post.load(user=User.on(Post.user_id == User.id))
            .query.where(and_(*conditions))
            .order_by(Post.id)
            .limit(data["limit"])
            .offset(data["offset"])
            .gino.all()
        )
        return web.json_response(PostSchema(many=True).dump(posts))
