import pytest
from app import app as flask_app, db
from models import User, Tweet # User をインポート

@pytest.fixture(scope='module')
def app():
    """
    テスト用のFlaskアプリケーションインスタンスを作成
    """
    # テスト用の設定に変更
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:", # インメモリDBを使用
        "WTF_CSRF_ENABLED": False # テストではCSRF保護を無効化することが多い
    })

    with flask_app.app_context():
        db.create_all() # テスト用DBテーブル作成

    yield flask_app

    # クリーンアップ (通常は不要だが念のため)
    # with flask_app.app_context():
    #     db.drop_all()


@pytest.fixture()
def client(app):
    """
    テスト用のHTTPクライアント
    """
    return app.test_client()


@pytest.fixture(autouse=True)
def setup_db(app):
    """
    各テストの前後にDBをクリーンアップ
    """
    with app.app_context():
        db.create_all()
        yield # テスト実行
        db.session.remove()
        db.drop_all()


# --- ヘルパー関数 ---
def register(client, username, email, password, password2):
    """ユーザー登録を行うヘルパー"""
    return client.post('/register', data=dict(
        username=username,
        email=email,
        password=password,
        password2=password2
    ), follow_redirects=True)

def login(client, username, password):
    """ユーザーログインを行うヘルパー"""
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    """ユーザーログアウトを行うヘルパー"""
    return client.get('/logout', follow_redirects=True)

# --- テスト ---

def test_index_get_logged_out(client):
    """
    GET / : ログアウト状態でトップページ表示をテスト
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b"Twitter Clone" in response.data
    assert "ログイン".encode('utf-8') in response.data # ログインリンクがある
    assert "登録".encode('utf-8') in response.data   # 登録リンクがある
    assert "新しいツイートを投稿".encode('utf-8') not in response.data # 投稿フォームはない
    assert "タイムライン".encode('utf-8') in response.data

def test_index_get_logged_in(client, app):
    """
    GET / : ログイン状態でトップページ表示をテスト
    """
    # テストユーザー作成・ログイン
    register(client, 'testuser', 'test@example.com', 'password', 'password')
    login(client, 'testuser', 'password')

    response = client.get('/')
    assert response.status_code == 200
    assert b"Twitter Clone" in response.data
    assert "こんにちは, testuser さん".encode('utf-8') in response.data # ユーザー名が表示される
    assert "ログアウト".encode('utf-8') in response.data # ログアウトリンクがある
    assert "ログイン".encode('utf-8') not in response.data # ログインリンクはない
    assert "登録".encode('utf-8') not in response.data   # 登録リンクはない
    assert "新しいツイートを投稿".encode('utf-8') in response.data # 投稿フォームがある
    assert "タイムライン".encode('utf-8') in response.data


def test_post_tweet_logged_in(client, app):
    """
    POST / : ログイン状態でツイート投稿をテスト
    """
    # テストユーザー作成・ログイン
    register(client, 'testuser', 'test@example.com', 'password', 'password')
    login(client, 'testuser', 'password')

    test_content = "This is a test tweet from a logged in user."
    response = client.post('/', data={'content': test_content}, follow_redirects=True)

    assert response.status_code == 200
    assert 'ツイートが投稿されました！'.encode('utf-8') in response.data # フラッシュメッセージ
    assert bytes(test_content, 'utf-8') in response.data # 投稿内容が表示される
    assert b'testuser' in response.data # 投稿者名が表示される

    # DBにも正しく保存されているか確認
    with app.app_context():
        tweets = Tweet.query.all()
        assert len(tweets) == 1
        assert tweets[0].content == test_content
        assert tweets[0].author.username == 'testuser' # authorリレーションを確認

def test_post_tweet_logged_out(client, app):
    """
    POST / : ログアウト状態でツイート投稿しようとするとログインページへリダイレクトされるかテスト
    """
    response = client.post('/', data={'content': 'Trying to tweet while logged out'}, follow_redirects=True)
    assert response.status_code == 200
    assert 'ツイートするにはログインが必要です。'.encode('utf-8') in response.data # フラッシュメッセージ
    assert 'ログイン'.encode('utf-8') in response.data # ログインページのタイトル
    assert b'Trying to tweet while logged out' not in response.data # ツイート内容は表示されない

    # DBに保存されていないことを確認
    with app.app_context():
        assert Tweet.query.count() == 0


def test_post_empty_tweet_logged_in(client, app):
    """
    POST / : ログイン状態で空のツイートを投稿できないことをテスト
    """
    # テストユーザー作成・ログイン
    register(client, 'testuser', 'test@example.com', 'password', 'password')
    login(client, 'testuser', 'password')

    response = client.post('/', data={'content': ''}, follow_redirects=True)

    assert response.status_code == 200
    assert 'ツイート内容を入力してください。'.encode('utf-8') in response.data # フラッシュメッセージ
    assert b'<div class="tweet">' not in response.data # ツイートは表示されない

    # DBにも保存されていないことを確認
    with app.app_context():
        assert Tweet.query.count() == 0


# --- 認証関連のテスト ---

def test_register(client, app):
    """ユーザー登録のテスト"""
    # GETリクエスト
    response = client.get('/register')
    assert response.status_code == 200
    assert 'ユーザー登録'.encode('utf-8') in response.data

    # POSTリクエスト (成功)
    response = register(client, 'newuser', 'new@example.com', 'password', 'password')
    assert response.status_code == 200
    assert '登録が完了しました。ログインしてください。'.encode('utf-8') in response.data
    assert 'ログイン'.encode('utf-8') in response.data # ログインページにリダイレクトされている

    # DBにユーザーが作成されたか確認
    with app.app_context():
        user = User.query.filter_by(username='newuser').first()
        assert user is not None
        assert user.email == 'new@example.com'
        assert user.check_password('password')

def test_register_existing_user(client, app):
    """既存のユーザー名/Emailでの登録失敗テスト"""
    register(client, 'testuser', 'test@example.com', 'password', 'password')

    # 同じユーザー名で登録
    response = register(client, 'testuser', 'other@example.com', 'password', 'password')
    assert response.status_code == 200
    assert "ユーザー名 &#39;testuser&#39; は既に使用されています。".encode('utf-8') in response.data # HTMLエンコードされた '
    assert 'ユーザー登録'.encode('utf-8') in response.data # 登録ページにとどまる

    # 同じEmailで登録
    response = register(client, 'anotheruser', 'test@example.com', 'password', 'password')
    assert response.status_code == 200
    assert "メールアドレス &#39;test@example.com&#39; は既に使用されています。".encode('utf-8') in response.data
    assert 'ユーザー登録'.encode('utf-8') in response.data

def test_register_password_mismatch(client):
    """パスワード不一致での登録失敗テスト"""
    response = register(client, 'testuser', 'test@example.com', 'pass1', 'pass2')
    assert response.status_code == 200
    assert 'パスワードが一致しません。'.encode('utf-8') in response.data
    assert 'ユーザー登録'.encode('utf-8') in response.data

def test_login_logout(client, app):
    """ログインとログアウトのテスト"""
    # まずユーザー登録
    register(client, 'loginuser', 'login@example.com', 'mypassword', 'mypassword')

    # GET ログインページ
    response = client.get('/login')
    assert response.status_code == 200
    assert 'ログイン'.encode('utf-8') in response.data

    # POST ログイン (成功)
    response = login(client, 'loginuser', 'mypassword')
    assert response.status_code == 200
    assert 'loginuserとしてログインしました。'.encode('utf-8') in response.data
    assert 'こんにちは, loginuser さん'.encode('utf-8') in response.data # トップページにリダイレクトされている

    # ログイン状態で /login にアクセスするとリダイレクト
    response = client.get('/login', follow_redirects=True)
    assert response.status_code == 200
    assert 'こんにちは, loginuser さん'.encode('utf-8') in response.data # トップページにいる

    # ログアウト
    response = logout(client)
    assert response.status_code == 200
    assert 'ログアウトしました。'.encode('utf-8') in response.data
    assert 'ログイン'.encode('utf-8') in response.data # トップページにリダイレクトされ、ログインリンクがある

    # ログアウト状態で /logout にアクセスするとログインページへリダイレクト
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    # Flask-Login のデフォルトメッセージは英語なのでバイトリテラルでOK
    assert b'Please log in to access this page.' in response.data
    assert 'ログイン'.encode('utf-8') in response.data # ログインページにいる

def test_login_invalid_credentials(client, app):
    """無効な認証情報でのログイン失敗テスト"""
    register(client, 'testuser', 'test@example.com', 'password', 'password')

    # 間違ったパスワード
    response = login(client, 'testuser', 'wrongpassword')
    assert response.status_code == 200
    assert 'ユーザー名またはパスワードが無効です。'.encode('utf-8') in response.data
    assert 'ログイン'.encode('utf-8') in response.data # ログインページにとどまる

    # 存在しないユーザー
    response = login(client, 'nosuchuser', 'password')
    assert response.status_code == 200
    assert 'ユーザー名またはパスワードが無効です。'.encode('utf-8') in response.data
    assert 'ログイン'.encode('utf-8') in response.data
