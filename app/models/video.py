from datetime import datetime
from app.extensions import db


class Video(db.Model):
    __tablename__ = "videos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video_url = db.Column(db.String(255), nullable=False)
    is_main = db.Column(db.Boolean, default=False)
    caption = db.Column(db.String(255))

    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Video {self.video_url}>"
