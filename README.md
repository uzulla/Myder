# Myder

**[重要] Makefileは廃止され、Python CLI（bin/myder）での利用に移行しました。**

---

## ディレクトリ構成

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

---

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

---

## 使い方

### 基本コマンド

```bash
bin/myder help
bin/myder build
bin/myder run --provider sample_provider --model <モデル名>
```

- Providerは `src/provider/` ディレクトリにPythonファイルを追加することで拡張できます。
- `bin/myder help` で利用可能なProvider一覧が表示されます。

### Providerの追加方法

1. `src/provider/` 配下に新しいPythonファイル（例: `my_provider.py`）を作成し、`Provider` クラスを実装してください。

   ```python
   # src/provider/my_provider.py
   class Provider:
       def run(self, model=None):
           # ここに処理を記述
           pass
   ```

2. `bin/myder run --provider my_provider` で実行できます。

---

## テスト

pytestでユニットテストを実行できます。

```bash
pytest
```

---

## Dockerビルド

Dockerイメージをビルドする場合は、以下を実行してください。

```bash
bin/myder build
```

---

## 注意事項

- Makefileやmyder.pyは廃止されました。今後は `bin/myder` をご利用ください。
- 標準ライブラリのみで動作します。
- Providerの追加・拡張が容易な構造です。
   ```
> Q: なぜ、ビルドしているのか？
> A: Aiderの公式コンテナはツールが足りない(curlすらない)のでつらいからです。そしてphpがあるのは作者の趣味です。


1. 都度環境変数 `OPENROUTER_API_KEY` を設定するか、`.env`ファイルをcloneしたDirectoryに作成し、OpenRouterのAPIキーを設定します：
   ```env
   OPENROUTER_API_KEY=your_api_key_here
   ```

## 使用例

1. プロジェクトディレクトリで以下のコマンドを実行：
   ```shell
   cd /path/to/your/project
   make -f /path/to/myder/Makefile run
   # あるいは後述の設定がしてあれば
   myder run
   ```

2. Aiderのシェルが起動します。

3. AIに対して自然言語で指示を出すことができます：
   詳しくはAiderのドキュメントを参照してください。

## オプションやタスク

### コマンド一覧を確認

利用可能なすべてのコマンドとその説明を表示するには、以下を実行してください：

```
make help
# または
myder help
```

これは初めて使う際や、利用可能なオプションを確認したい場合に役立ちます。

### 基本的な実行方法

```
make run
```

デフォルトのGemini-2.5-pro-exp-03-25モデルを使用して実行：

> 特に、このモデルが推奨ということではありません。

### 特定のモデルを指定して実行

```
make run MODEL=anthropic/claude-3-opus
```

利用可能なモデルは[OpenRouterのモデル一覧](https://openrouter.ai/models)から確認できます。

### マウントせずに実行

```
make run NOMOUNT=1
```

つまり、ホストを破壊しません。

### 自動確認モードで実行（危険）

```
make run FORCE_YES=1
```

OKをEnterで押すのにつかれた人向け

### オプションを組み合わせて実行

```
make run MODEL=anthropic/claude-3-haiku-20240307 FORCE_YES=1 NOMOUNT=1
```

## 特殊な使い方(主にデバッグ用)

### Dockerコンテナ内でbashを実行

```
make run-bash
```

### マウントせずにbashを実行

```
make run-bash NOMOUNT=1
```

### Root権限でコンテナ内のbashを実行

```
make run-root-bash
```

### マウントせずにRoot権限でコンテナ内のbashを実行

```
make run-root-bash NOMOUNT=1
```

このコマンドの修正はコマンド再実行時に保存されません。必要ならDockerを修正してビルドしなおしてください。

### Dockerイメージをビルド

```
make build
```

### どこからでも簡単にMyderを使用する

どのディレクトリからでも簡単にMyderを使えるようにするには、シェルのエイリアスを設定すると便利です：

```bash
alias myder="make -f ~/dev/myder/Makefile"
```

このエイリアスを`.bashrc`、`.zshrc`などのシェル設定ファイルに追加することで、永続的に使用できます：

```bash
echo 'alias myder="make -f ~/dev/myder/Makefile"' >> ~/.bashrc
# または
echo 'alias myder="make -f ~/dev/myder/Makefile"' >> ~/.zshrc
```

設定後は、任意のディレクトリから以下のように使用できます：

```bash
# 基本実行
myder run

# モデル指定
myder run MODEL=anthropic/claude-3-opus

# オプション組み合わせ
myder run MODEL=anthropic/claude-3-haiku-20240307 FORCE_YES=1 NOMOUNT=1
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
