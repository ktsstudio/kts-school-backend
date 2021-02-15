from hashlib import md5

import pytest

from blog_app.post.models import Post
from blog_app.user.models import User
from blog_app.utils import now


@pytest.fixture
async def user():
    return await User.create(
        username="test", password=md5(b"1234").hexdigest(), created=now()
    )


@pytest.fixture
async def user2():
    return await User.create(
        username="test2", password=md5(b"1234").hexdigest(), created=now()
    )
