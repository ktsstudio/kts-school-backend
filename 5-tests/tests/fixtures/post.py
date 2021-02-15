import pytest

from blog_app.post.models import Post
from blog_app.user.models import User
from blog_app.utils import now


@pytest.fixture
async def post(user):
    return await Post.create(user_id=user.id, created=now(), text="Test post")


@pytest.fixture
async def posts(user: User, user2: User):
    await Post.create(user_id=user.id, created=now(), text="Test post"),
    await Post.create(user_id=user2.id, created=now(), text="Test post 2"),
    return await Post.load(
        user=User.on(Post.user_id == User.id)
    ).query.gino.all()
