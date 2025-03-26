import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash # Userモデルで使っているので不要かもだが念のため

# アプリケーションの設定
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# --- 重要: セッション管理のためのシークレットキーを設定 ---
# 実際のアプリケーションでは、環境変数などから読み込むべきです
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key') # 環境変数があればそれを使う
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tweets.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # 未ログイン時にリダイレクトされるビュー関数名

# データベースモデルのインポート (Userもインポート)
from models import User, Tweet

@login_manager.user_loader
def load_user(user_id):
    """Flask-Login がユーザーをロードするための関数"""
    return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    ツイートの表示と投稿処理 (ログインユーザーのみ投稿可能)
    """
    if request.method == 'POST':
        # ログインしていない場合は投稿できないようにする
        if not current_user.is_authenticated:
            flash('ツイートするにはログインが必要です。', 'warning')
            return redirect(url_for('login'))

        content = request.form.get('content')
        if content:
            # ログイン中のユーザー (current_user) に紐付けてツイートを作成
            new_tweet = Tweet(content=content, author=current_user)
            db.session.add(new_tweet)
            db.session.commit()
            flash('ツイートが投稿されました！', 'success')
            return redirect(url_for('index')) # 投稿後はリダイレクト
        else:
            flash('ツイート内容を入力してください。', 'danger')

    # GETリクエストの場合、または投稿後にツイート一覧を表示
    # Tweetモデルのauthorリレーションを効率的に読み込むために joinedload を使用
    from sqlalchemy.orm import joinedload
    tweets = Tweet.query.options(joinedload(Tweet.author)).order_by(Tweet.created_at.desc()).all()
    return render_template('index.html', tweets=tweets)


@app.route('/user/<username>')
@login_required # プロフィールを見るにはログインが必要 (任意、公開プロフィールなら不要)
def user(username):
    """ユーザープロフィールページ"""
    # ユーザーが存在するか確認
    user = User.query.filter_by(username=username).first_or_404() # 見つからなければ404エラー

    # そのユーザーのツイートを取得 (新しい順)
    # Tweetモデルのauthorリレーションを使ってフィルタリング
    tweets = user.tweets.order_by(Tweet.created_at.desc()).all()

    return render_template('user.html', user=user, tweets=tweets)


@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    """指定したユーザーをフォローする"""
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f'ユーザー {username} が見つかりません。', 'warning')
        return redirect(url_for('index'))
    if user == current_user:
        flash('自分自身をフォローすることはできません。', 'warning')
        return redirect(url_for('user', username=username))

    current_user.follow(user)
    db.session.commit()
    flash(f'{username} をフォローしました。', 'success')
    # 元のプロフィールページ、または指定されたリダイレクト先へ
    return redirect(request.referrer or url_for('user', username=username))


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    """指定したユーザーのフォローを解除する"""
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f'ユーザー {username} が見つかりません。', 'warning')
        return redirect(url_for('index'))
    if user == current_user:
        flash('自分自身をアンフォローすることはできません。', 'warning')
        return redirect(url_for('user', username=username))

    current_user.unfollow(user)
    db.session.commit()
    flash(f'{username} のフォローを解除しました。', 'info')
    # 元のプロフィールページ、または指定されたリダイレクト先へ
    return redirect(request.referrer or url_for('user', username=username))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """ユーザー登録"""
    if current_user.is_authenticated:
        return redirect(url_for('index')) # ログイン済みならトップへ

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        # バリデーション (簡易)
        error = None
        if not username:
            error = 'ユーザー名が必要です。'
        elif not email:
            error = 'メールアドレスが必要です。'
        elif not password:
            error = 'パスワードが必要です。'
        elif password != password2:
            error = 'パスワードが一致しません。'
        elif User.query.filter_by(username=username).first() is not None:
            error = f"ユーザー名 '{username}' は既に使用されています。"
        elif User.query.filter_by(email=email).first() is not None:
            error = f"メールアドレス '{email}' は既に使用されています。"

        if error is None:
            # ユーザー作成
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('登録が完了しました。ログインしてください。', 'success')
            return redirect(url_for('login'))
        else:
            flash(error, 'danger')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ユーザーログイン"""
    if current_user.is_authenticated:
        return redirect(url_for('index')) # ログイン済みならトップへ

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on' # チェックボックスの値を確認

        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(password):
            flash('ユーザー名またはパスワードが無効です。', 'danger')
            return redirect(url_for('login'))

        # ユーザーをログインさせる
        login_user(user, remember=remember)
        flash(f'{user.username}としてログインしました。', 'success')

        # ログイン後にリダイレクトするページ (nextパラメータがあればそこへ)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html')


@app.route('/logout')
@login_required # ログイン必須
def logout():
    """ユーザーログアウト"""
    logout_user()
    flash('ログアウトしました。', 'info')
    return redirect(url_for('index'))


# URLの安全性を確認するためのヘルパー (loginリダイレクト用)
from urllib.parse import urlparse, urljoin
def url_parse(url):
    return urlparse(url)

def is_safe_url(target):
   ref_url = urlparse(request.host_url)
   test_url = urlparse(urljoin(request.host_url, target))
   return test_url.scheme in ('http', 'https') and \
          ref_url.netloc == test_url.netloc

# アプリケーションコンテキスト内でデータベース作成を行うためのコマンド
# flask shell で Python インタプリタを起動し、以下のコマンドを実行
# >>> from app import db
# >>> db.create_all()

if __name__ == '__main__':
    # debug=True は開発時にのみ使用し、本番環境ではFalseに設定する
    app.run(debug=True, host='0.0.0.0') # 外部からもアクセス可能にする場合 host='0.0.0.0' を追加
