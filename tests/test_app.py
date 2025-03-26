import pytest
from app import app as flask_app, db, Tweet

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


def test_index_get(client):
    """
    GET / : トップページが正常に表示されるかテスト
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b"Twitter Clone" in response.data
    assert "新しいツイートを投稿".encode('utf-8') in response.data
    assert "タイムライン".encode('utf-8') in response.data


def test_index_post_tweet(client, app):
    """
    POST / : 新しいツイートが投稿できるかテスト
    """
    test_username = "testuser"
    test_content = "This is a test tweet."
    response = client.post('/', data={
        'username': test_username,
        'content': test_content
    }, follow_redirects=True) # follow_redirects=True でリダイレクト後のページを取得

    assert response.status_code == 200
    assert bytes(test_username, 'utf-8') in response.data
    assert bytes(test_content, 'utf-8') in response.data

    # DBにも正しく保存されているか確認
    with app.app_context():
        tweets = Tweet.query.all()
        assert len(tweets) == 1
        assert tweets[0].username == test_username
        assert tweets[0].content == test_content


def test_index_post_empty_tweet(client, app):
    """
    POST / : 内容が空のツイートは投稿できないことをテスト
    """
    response = client.post('/', data={
        'username': 'testuser',
        'content': ''
    }, follow_redirects=True)

    assert response.status_code == 200
    # 空のツイートは表示されないはず
    assert b'testuser' not in response.data
    assert b'<div class="tweet">' not in response.data # ツイート表示エリアがないことを確認

    # DBにも保存されていないことを確認
    with app.app_context():
        tweets = Tweet.query.all()
        assert len(tweets) == 0
