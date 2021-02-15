from blog_app.store.database import db


class Post(db.Model):
    __tablename__ = "post"

    id = db.Column(db.BigInteger(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)
    text = db.Column(db.Text(), nullable=False)
    created = db.Column(db.DateTime(timezone=True), nullable=False)
