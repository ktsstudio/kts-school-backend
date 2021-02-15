from aiohttp import web

from blog_app.user import views as user_views
from blog_app.post import views as post_views


def setup_routes(app: web.Application) -> None:
    app.router.add_view("/user.me", user_views.MeView)
    app.router.add_view("/user.register", user_views.RegisterView)
    app.router.add_view("/user.login", user_views.LoginView)
    app.router.add_view("/user.external", user_views.ExternalView)

    app.router.add_view("/post.create", post_views.CreatePostView)
    app.router.add_view("/post.list", post_views.PostListView)
