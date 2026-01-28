# Audio Splitter for Gemini API

このスクリプトは、Google Gemini API などのファイルサイズ制限（例: 100MB）を超える大きな WAV 音声ファイルを、指定したサイズ以下に自動分割するためのツールです。

### 開発の背景

Gemini API に音声データを送信する際、1ファイルあたりのサイズ制限に抵触することがあります。このプログラムは、音声の品質を維持したまま、指定したファイル容量（デフォルト 95MB）に収まるように時間軸で分割を行います。

### 機能

* WAV ファイルを読み込み、指定の MB 単位で分割。
* メタデータに基づいた正確なサイズ計算。
* 分割されたファイルは `split_chunks` フォルダに自動保存。

### 前提条件

このスクリプトは Python で動作し、音声操作のために `pydub` を使用します。また、バックエンドに `ffmpeg` が必要です。

#### 1. ライブラリのインストール

```bash
pip install pydub

```

#### 2. ffmpeg のインストール

* **Mac (Homebrew):** `brew install ffmpeg`
* **Windows:** [Gyan.dev](https://www.gyan.dev/ffmpeg/builds/) 等からバイナリをダウンロードし、パスを通してください。

### 使い方

1. スクリプト内の `split_wav_by_size("path/to/your/file.wav")` のパスを対象のファイルに書き換えます。
2. スクリプトを実行します。
```bash
python split_audio.py

```


3. 実行完了後、`split_chunks/` フォルダ内に分割された WAV ファイルが生成されます。

### 注意事項

* **フォーマット:** 現在は WAV 形式専用です。
* **余裕を持った設定:** 通信時のオーバーヘッドを考慮し、デフォルトの制限値を 95MB に設定しています。

---
