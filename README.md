# Myder

Myder（マイダー）は、[Aider](https://aider.chat/)をDocker環境で実行し、[OpenRouter](https://openrouter.ai/)経由で様々なAIモデルと対話するためのラッパーツールです。

Dockerを用いることでセットアップを容易にし、実行時にAiderが参照出来るファイルを実行時ディレクトリに限定もできます。

また、OpenRouterが提供するModelの指定も楽にできます。

## 用意する前提条件

- Docker
- OpenRouterのAPIキー ([ここで生成できます](https://openrouter.ai/settings/keys))

### Linuxの場合

Bind mountする都合上、以下指定を追加したほうがよいかもしれません

```makefile
--user $(shell id -u):$(shell id -g)
```

## セットアップ

1. このリポジトリをクローンします：
   ```shell
   git clone https://github.com/uzulla/myder.git
   cd myder
   ```

2. Dockerイメージを取得します(アップデートのためにたまに実行してください)：
   ```shell
   make pull
   ```

3. 都度環境変数 `OPENROUTER_API_KEY` を設定するか、`.env`ファイルをcloneしたDirectoryに作成し、OpenRouterのAPIキーを設定します：
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

### 基本的な実行方法

デフォルトのGemini-2.5-pro-expモデルを使用して実行：

```
make run
```

> 特に、このモデルが推奨ということではありません。

### 特定のモデルを指定して実行

```
make run-model MODEL=anthropic/claude-3-opus
```

利用可能なモデルは[OpenRouterのモデル一覧](https://openrouter.ai/models)から確認できます。

## 特殊な使い方(主にデバッグ用)

### Dockerコンテナ内でbashを実行

```
make run-bash
```

### Root権限でコンテナ内のbashを実行

```
make run-root-bash
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
myder run-model MODEL=anthropic/claude-3-opus
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
性能の良いものをつかいましょう。たとえば `Claude 3.7 sonet` です
