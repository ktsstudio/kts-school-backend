import datetime
import uuid

from freezegun import freeze_time

from blog_app.user.models import User, Session
from tests.conftest import DEFAULT_TIME, authenticate


def user2dict(user: User):
    return {
        "username": user.username,
        "created": user.created.isoformat(),
        "id": user.id,
    }


class TestRegisterView:
    async def test_success(self, cli):
        data = {"username": "test", "password": "1234"}
        response = await cli.post("/user.register", json=data)
        assert response.status == 200
        user = await User.query.gino.first()
        assert await response.json() == user2dict(user)

    async def test_already_exists(self, cli, user: User):
        data = {"username": user.username, "password": "1234"}
        response = await cli.post("/user.register", json=data)
        assert response.status == 400
        assert await response.json() == {"code": "user_already_exists"}


class TestLoginView:
    async def test_success(self, cli, user: User, mocker, freeze_t):
        token = "0" * 32
        mock_uuid = mocker.patch.object(uuid, "uuid4", autospec=True)
        mock_uuid.return_value = uuid.UUID(hex=token)
        data = {"username": user.username, "password": "1234"}
        response = await cli.post("/user.login", json=data)
        assert response.status == 200
        session = await Session.query.where(Session.key == token).gino.first()
        assert session.user_id == user.id
        assert session.expires == DEFAULT_TIME + datetime.timedelta(days=1)
        assert await response.json() == {"token": token}

    async def test_invalid_credentials(self, cli, user: User):
        data = {"username": user.username, "password": "12345"}
        response = await cli.post("/user.login", json=data)
        assert response.status == 400
        response_data = await response.json()
        assert response_data == {"code": "invalid_credentials"}


class TestMeView:
    async def test_unauthorized(self, cli):
        response = await cli.get("/user.me")
        assert response.status == 401
        assert await response.json() == {"code": "unauthorized"}

    async def test_authorized(self, cli, user: User):
        async with authenticate(cli, user):
            response = await cli.get("/user.me")
        assert response.status == 200
        assert await response.json() == user2dict(user)


class TestAuthorization:
    async def test_authorized(self, cli, user: User):
        async with authenticate(cli, user):
            with freeze_time(DEFAULT_TIME + datetime.timedelta(days=3)):
                response = await cli.get("/user.me")
        assert response.status == 401
        assert await response.json() == {"code": "unauthorized"}


class TestExternal:
    async def test_success(self, cli, mock_response):
        mock_response.get(
            "https://www.metaweather.com/api/location/44418/",
            status=200,
            payload={"temp": 23},
        )
        response = await cli.get("/user.external")
        assert response.status == 200
        assert await response.json() == {"temp": 23}
