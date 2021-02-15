from typing import List

import pytest

from blog_app.post.models import Post
from blog_app.user.models import User
from tests.user.test_views import user2dict


def post2dict(post: Post):
    return {
        "text": post.text,
        "id": post.id,
        "created": post.created.isoformat(),
        "user": user2dict(post.user),
    }


class TestPostListView:
    @pytest.mark.parametrize("params,expected_idxs", [
        [{}, [0, 1]],
        [{"limit": 1}, [0]],
        [{"offset": 1}, [1]],
        [{"user_id": 1}, [1]]
    ])
    async def test_success(
        self, cli, posts: List[Post], user: User, user2, params: dict, expected_idxs
    ):
        users = [user, user2]
        if "user_id" in params:
            params["user_id"] = users[params["user_id"]].id
        response = await cli.get("/post.list", params=params)
        assert response.status == 200
        assert await response.json() == [post2dict(posts[idx]) for idx in expected_idxs]
