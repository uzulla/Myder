# Myder

Myderは、DockerコンテナでAider（AIコーディングアシスタント）を簡単に実行するためのラッパーツールです。プログラミングや開発作業をAIによってアシストします。必要なツール類が揃ったDockerイメージを使用することで、環境構築の手間を省きます。

## インストール・セットアップ

1. このリポジトリをクローンします：

   ```bash
   git clone https://github.com/uzulla/myder.git
   cd myder
   ```

2. 依存パッケージは不要です（標準ライブラリのみで動作）。

3. `bin/myder` に実行権限がない場合は付与してください：

   ```bash
   chmod +x bin/myder
   ```

4. `bin/` ディレクトリをPATHに追加するか、`bin/myder` を直接実行してください。

あるいは以下のようなAliasでもよいでしょう

```bash
alias myder='/path/to/myder/bin/myder'
```

## 使用例

1. プロジェクトディレクトリで以下のコマンドを実行：
   ```shell
   cd /path/to/your/project
   myder run
   ```

2. Aiderのシェルが起動します。

3. AIに対して自然言語で指示を出すことができます：
   詳しくはAiderのドキュメントを参照してください。

## オプションやタスク

### 基本的な実行方法

```
myder run
```

デフォルトのGemini-2.5-pro-exp-03-25モデルを使用して実行：

> 特に、このモデルが推奨ということではありません。

### 特定のモデルを指定して実行

```
myder run --model anthropic/claude-3-opus
```

利用可能なモデルは[OpenRouterのモデル一覧](https://openrouter.ai/models)から確認できます。

### マウントせずに実行

```
myder run --nomount
```

つまり、ホストを破壊しません。

### 自動確認モードで実行（危険）

```
myder run --force-yes
```

OKをEnterで押すのにつかれた人向け

### オプションを組み合わせて実行

```
myder run --model anthropic/claude-3-haiku-20240307 --force-yes --nomount
```

### コマンド一覧を確認

利用可能なすべてのコマンドとその説明を表示するには、以下を実行してください：

```
myder --help
```

これは初めて使う際や、利用可能なオプションを確認したい場合に役立ちます。

## Dockerイメージをビルド

```
myder build
```

## どこからでも簡単にMyderを使用する

どのディレクトリからでも簡単にMyderを使えるようにするには、`bin`ディレクトリをPATHに追加するか、シンボリックリンクを作成すると便利です：

```bash
# PATHに追加する場合（.bashrcや.zshrcに記述）
export PATH="/path/to/myder/bin:$PATH"

# またはシンボリックリンクを作成
ln -s /path/to/myder/bin/myder /usr/local/bin/myder
```

設定後は、任意のディレクトリから以下のように使用できます：

```bash
# 基本実行
myder run

# モデル指定
myder run --model anthropic/claude-3-opus

# オプション組み合わせ
myder run --model anthropic/claude-3-haiku-20240307 --force-yes --nomount
```

## APIキーの設定

都度環境変数 `OPENROUTER_API_KEY` を設定するか、`.env`ファイルをクローンしたディレクトリに作成し、OpenRouterのAPIキーを設定します：
```env
OPENROUTER_API_KEY=your_api_key_here
```

## Aiderの仕様

### Aiderの設定ファイル

たとえば以下のようなファイルが生成されますが、これらはAider実行時に生成されるファイルであり、削除しても問題ありません。

```
.aider
.aider.chat.history.md
.aider.input.history
```

### モデル選定

AiderをClaude codeのようにつかう(プログラミングに使う)場合、Modelの選定が重要です。
性能の良いものをつかいましょう。たとえば `anthropic/claude-3-7-sonnet` です

---

## 技術的な情報

### ディレクトリ構成

```
bin/
  myder            # CLI実行ファイル（Shebang付、直接実行可能）
src/
  myder_core.py    # コアロジック
  provider/        # Provider追加用ディレクトリ
    __init__.py
    sample_provider.py
tests/
  test_myder_core.py # pytest形式テスト
```

### Providerの追加方法

1. `src/provider/` 配下に新しいPythonファイル（例: `my_provider.py`）を作成し、`Provider` クラスを実装してください。

   ```python
   # src/provider/my_provider.py
   class Provider:
       def run(self, model=None):
           # ここに処理を記述
           pass
   ```

2. `myder run --model <モデル名>` で実行できます。

### テスト

pytestでユニットテストを実行できます。

```bash
pytest
```

### その他特記事項

> Q: なぜ、コンテナをビルドしているのか？
> A: Aiderの公式コンテナはツールが足りない(curlすらない)のでつらいからです。そしてphpまであるのは作者の趣味です。
