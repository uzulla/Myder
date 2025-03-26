from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db # db を先にインポート
from datetime import datetime

# フォロー関係を表す関連テーブル
# 自己参照多対多関係: User が User をフォローする
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

# UserMixin を継承して Flask-Login の標準メソッドを組み込む
class User(UserMixin, db.Model):
    """
    ユーザー情報を格納するモデル
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False) # 簡単のため必須＆ユニークに
    password_hash = db.Column(db.String(128))
    # UserからTweetへのリレーションシップ
    tweets = db.relationship('Tweet', backref='author', lazy='dynamic', cascade="all, delete-orphan")

    # フォロー/フォロワー関係の定義
    # secondary で関連テーブルを指定
    # primaryjoin と secondaryjoin で関連テーブルのどのカラムが自分（左側）と相手（右側）に対応するか指定
    # backref で User.followers として自分をフォローしているユーザーリストにアクセス可能に
    # lazy='dynamic' でクエリを返すようにする
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

    # --- フォロー/アンフォロー用メソッド ---
    def follow(self, user):
        """指定したユーザーをフォローする"""
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        """指定したユーザーのフォローを解除する"""
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        """指定したユーザーをフォローしているか確認する"""
        # self.followed 関係を通じて、指定した user.id が存在するかチェック
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    # --- フォローしているユーザーのツイートを取得するメソッド ---
    def followed_posts(self):
        """フォローしているユーザー（自分自身を含む）のツイートを取得する"""
        # フォローしているユーザーのツイートを取得
        followed = Tweet.query.join(
            followers, (followers.c.followed_id == Tweet.user_id)).filter(
                followers.c.follower_id == self.id)
        # 自分のツイートを取得
        own = Tweet.query.filter_by(user_id=self.id)
        # 結合して新しい順に並び替え
        return followed.union(own).order_by(Tweet.created_at.desc())


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
