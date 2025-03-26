import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# アプリケーションの設定
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tweets.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# データベースモデルのインポート
from models import Tweet

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    ツイートの表示と投稿処理
    """
    if request.method == 'POST':
        username = request.form.get('username', '名無しさん') # 簡単のためユーザー名はフォームから取得
        content = request.form.get('content')

        if content:
            new_tweet = Tweet(username=username, content=content)
            db.session.add(new_tweet)
            db.session.commit()
            return redirect(url_for('index')) # 投稿後はリダイレクト

    # GETリクエストの場合、または投稿後にツイート一覧を表示
    tweets = Tweet.query.order_by(Tweet.created_at.desc()).all()
    return render_template('index.html', tweets=tweets)

# アプリケーションコンテキスト内でデータベース作成を行うためのコマンド
# flask shell で Python インタプリタを起動し、以下のコマンドを実行
# >>> from app import db
# >>> db.create_all()

if __name__ == '__main__':
    # debug=True は開発時にのみ使用し、本番環境ではFalseに設定する
    app.run(debug=True, host='0.0.0.0') # 外部からもアクセス可能にする場合 host='0.0.0.0' を追加
