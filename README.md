# Beatrice Trainer with Modal

このプロジェクトは、[fierce-cats/beatrice-trainer](https://huggingface.co/fierce-cats/beatrice-trainer) のコードをベースに、Modal 上で Beatrice モデルの学習を実行するためのセットアップ例です。  
このリポジトリには Modal でのジョブ実行用スクリプト `modal_train.py` が含まれており、学習データ（data ディレクトリ）と学習済みモデル（out_dir ディレクトリ）の永続化のためのディレクトリを用意します。

> **注意**:
> 一つでも手順を間違えたら動かない可能性大です。

## ディレクトリ構成

リポジトリのルートは以下のような構成となります。

```
beatrice-trainer/
├── LICENSE
├── README.md         # このファイル
└── modal_train.py    # Modal で学習を実行するためのスクリプト
```

## セットアップ手順

### 0. Modalのセットアップ

Modal を利用するには、Modal CLI のインストールと初期設定が必要です。以下の手順に従ってセットアップしてください。

1. **Modal CLI のインストール**  
Python 環境に Modal CLI をインストールします。  
```bash
pip install modal
```
2. **Modal アカウントの認証**  
初回セットアップでは、以下のコマンドを実行してブラウザで認証を行います。
```bash
modal setup
```
表示される URL にアクセスし、Modal アカウントと GitHub アカウントなどを連携してください。

### 1. リポジトリのダウンロード

Git LFS を使用してリポジトリをクローンします。ターミナルで以下のコマンドを実行してください。

```bash
git lfs install
git clone https://huggingface.co/fierce-cats/beatrice-trainer
cd beatrice-trainer
```

ダウンロードしましたら以下のコマンドを実行してpyproject.tomlファイルの記述を一部変更します。
```bash
sed -i 's/python = ">=3.9"/python = ">=3.10"/g' pyproject.toml
```
> **注意**:  
> - macOS を使用している場合、`sed -i` オプションの使い方が異なるため、以下のようにバックアップ拡張子を指定する必要があります:
>
>   ```bash
>   sed -i '' 's/python = ">=3.9"/python = ">=3.10"/g' pyproject.toml
>   ```

### 2. 必要ファイルの配置とディレクトリの作成

- **modal_train.py の配置**  
  このリポジトリのルートディレクトリに `modal_train.py` を配置します。  
  （すでに配置済みの場合はこの手順は不要です。）
```bash
git clone https://github.com/smizuoch/modal-beatrice-trainer.git
mv ./modal-beatrice-trainer/modal_train.py ./
```

- **学習データディレクトリの作成 (`data/`)**  
  学習データは各話者ごとにサブディレクトリを作成して配置してください。  
  例:
  ```
  data/
  ├── speaker1
  │   ├── sample1.wav
  │   └── sample2.wav
  └── speaker2
      ├── sample1.wav
      └── sample2.wav
  ```
  ```bash
  mkdir data
  ```

- **成果物保存ディレクトリの作成 (`model/`)**  
  学習中に生成される重みなどの成果物を保存するためのディレクトリです。  
  このディレクトリは Modal の永続ボリュームとしてマウントするために使用します。
```bash
mkdir model
```

このボリュームは、Modal 実行時に成果物保存用ディレクトリとして `/workspace/model` にマウントします。

### 3. modal_train.py の実行方法

Modal 上で学習ジョブを実行するには、以下のようにコマンドラインから実行します。

```bash
modal run modal_train.py --data-dir ./data --out-dir /workspace/model
```

- `--data-dir` : 学習データが配置されたディレクトリ（例: `./data`）を指定します。

## modal_train.py の概要

`modal_train.py` は以下の処理を行います。

1. **イメージの構築**  
   - Python 3.10-slim ベースのイメージを利用
   - 必要な apt パッケージ（`g++`, `build-essential`）および pip パッケージ（`poetry` など）をインストール

2. **マウント設定**  
   - リポジトリ全体を `/workspace` にマウント
   - Modal Volume（永続ボリューム "beatrice-models"）を `/workspace/out_dir` にマウント

3. **依存関係のインストール**  
   - コンテナ内で `poetry config virtualenvs.create false` を実行し、仮想環境を作成せずシステムに依存関係をインストール
   - `poetry install` により、`pyproject.toml` に記載された依存関係（torch、torchaudio、tqdm、tensorboard、pyworld など）がインストールされる

4. **学習スクリプトの実行**  
   - `python3 beatrice_trainer -d <data_dir> -o /workspace/out_dir` を実行して、学習を開始します

## Modal の実行例

以下は、実際に Modal 上でジョブを実行する際のコマンド例です。

```bash
modal run modal_train.py --data-dir ./data --out-dir /workspace/model
```

Modal のジョブが正常に実行されると、学習済みの重みが永続ボリューム上の `/workspace//out_dir` に保存されます。
https://modal.com/storage/ リンクにアクセスすると手順通りに行なっていれば `beatrice-models` というボリューム上に `checkpoint_data_00000001.pt` のような形でモデルが出来上がります。
ダウンロードしたい場合は以下のコマンドでダウンロードできます。
```bash
modal volume get beatrice-models checkpoint_latest.pt
```
最終出力のモデルをダウンロードする例  

愚直に全てダウンロードするなら以下のコマンドでできます。
```bash
modal volume get beatrice-models /
```
間違えてデスクトップやダウンロードで行うと大変なことになるので新しいディレクトリに移動して実行することをお勧めします。

## ライセンス

このプロジェクトは MIT License のもとで公開されています。詳細は [LICENSE](./LICENSE) をご覧ください。

## お問い合わせ

ご質問やフィードバックは、GitHub の [Issues](https://github.com/smizuoch/modal-beatrice-trainer/issues) でお知らせください。できる限り対応します。

## 支援

当方リソースやお金をあまり持ってない学生のためパソコンやリソース、資金を支援していただける方がいれば連絡いただけたら嬉しいです。
