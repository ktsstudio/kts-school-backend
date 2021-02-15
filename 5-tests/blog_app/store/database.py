from gino import Gino

db = Gino()

from blog_app.user.models import *
from blog_app.post.models import *
