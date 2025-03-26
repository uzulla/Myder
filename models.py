from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db # db を先にインポート
from datetime import datetime

# UserMixin を継承して Flask-Login の標準メソッドを組み込む
class User(UserMixin, db.Model):
    """
    ユーザー情報を格納するモデル
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False) # 簡単のため必須＆ユニークに
    password_hash = db.Column(db.String(128))
    # UserからTweetへのリレーションシップ (Userが削除されたらTweetも削除される)
    tweets = db.relationship('Tweet', backref='author', lazy='dynamic', cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Tweet(db.Model):
    """
    ツイート情報を格納するモデル
    """
    id = db.Column(db.Integer, primary_key=True)
    # username は User モデルとのリレーション経由で取得するため不要になる
    # username = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(280), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, index=True, default=datetime.utcnow) # index=True を追加
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Userテーブルへの外部キー

    def __repr__(self):
        # authorリレーションを使ってユーザー名を表示
        return f'<Tweet {self.id} by {self.author.username}>'
