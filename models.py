from app import db
from datetime import datetime

class Tweet(db.Model):
    """
    ツイート情報を格納するモデル
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(280), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Tweet {self.id}: {self.username}>'
