WAVからMP3への変換、そしてサイズ制限（100MB）に基づいた分割処理を組み込んだコードに修正しました。

MP3はWAVに比べて劇的にファイルサイズが小さくなるため、Geminiのトークン消費を抑えつつ、長時間の録音を効率的に扱えるようになります。

---

## 修正版 Pythonコード

このコードでは、指定したビットレート（デフォルト128kbps）を基準に、100MBを超えないような時間を逆算して分割します。

```python
import os
import math
from pydub import AudioSegment

def process_audio_for_gemini(file_path, max_size_mb=95, bitrate="128k"):
    """
    WAVをMP3に変換し、必要に応じて100MB以下に分割する。
    """
    if not os.path.exists(file_path):
        print(f"エラー: ファイル {file_path} が見つかりません。")
        return

    # 音声ファイルの読み込み
    print(f"ファイルを読み込み中: {file_path}")
    audio = AudioSegment.from_wav(file_path)
    
    # 出力ディレクトリの作成
    output_dir = "converted_mp3"
    os.makedirs(output_dir, exist_ok=True)

    # ビットレートから1秒あたりのバイト数を計算
    # 128k bps = 128,000 bits per second = 16,000 bytes per second
    bitrate_int = int(bitrate.replace('k', '')) * 1000
    bytes_per_second = bitrate_int / 8
    
    # 指定MBに相当する秒数を計算
    target_size_bytes = max_size_mb * 1024 * 1024
    max_duration_per_chunk_ms = math.floor((target_size_bytes / bytes_per_second) * 1000)

    total_duration_ms = len(audio)

    # 1ファイルで収まるかチェック
    if total_duration_ms <= max_duration_per_chunk_ms:
        # 分割不要
        output_name = os.path.join(output_dir, "output_audio.mp3")
        audio.export(output_name, format="mp3", bitrate=bitrate)
        print(f"変換完了 (分割なし): {output_name}")
    else:
        # 分割実行
        print(f"ファイルサイズが大きいため分割を開始します...")
        for i, start_ms in enumerate(range(0, total_duration_ms, max_duration_per_chunk_ms)):
            chunk = audio[start_ms : start_ms + max_duration_per_chunk_ms]
            chunk_name = os.path.join(output_dir, f"chunk_{i+1}.mp3")
            
            chunk.export(chunk_name, format="mp3", bitrate=bitrate)
            print(f"保存完了: {chunk_name} ({len(chunk)/1000/60:.2f}分)")

if __name__ == "__main__":
    # 2026年1月28日の録音データを確認
    process_audio_for_gemini("./20260128_voicedata.wav")

```

---

## README.md (更新版)

# Audio Converter & Splitter for Gemini

このツールは、重い WAV 音声ファイルを **MP3 形式に軽量化** し、さらに Google Gemini API の制限（100MB）に合わせて **自動分割** するためのスクリプトです。

### なぜ MP3 に変換するのか？

1. **ファイルサイズの削減**: WAV 形式は非常に容量が大きいため、API の上限に達しやすくなります。MP3 にすることで、音質を維持しつつ容量を約 1/10 以下に抑えられます。
2. **コストと効率**: Gemini API で音声を処理する際、ファイルサイズが小さいほどアップロードが高速になり、処理待ち時間を短縮できます。

### 主な機能

* **自動 MP3 変換**: 指定したビットレート（128kbps）で WAV から MP3 へ変換します。
* **インテリジェント分割**: 変換後のファイルサイズを予測し、100MB を超える場合は自動で複数の MP3 ファイルに分割して出力します。
* **ディレクトリ管理**: 生成されたファイルは `converted_mp3` フォルダに整理されます。

### セットアップ

#### 1. 依存ライブラリのインストール

音声処理ライブラリ `pydub` を使用します。

```bash
pip install pydub

```

#### 2. ffmpeg の準備

MP3 へのエンコードには `ffmpeg` が必須です。

* **Mac**: `brew install ffmpeg`
* **Windows**: [Gyan.dev](https://www.gyan.dev/ffmpeg/builds/) から実行ファイルをダウンロードし、システム環境変数（Path）に追加してください。

### 使い方

1. プロジェクトのルートディレクトリに変換したい `.wav` ファイルを配置します。
2. スクリプト内のファイルパスを修正します（例: `process_audio_for_gemini("./your_file.wav")`）。
3. スクリプトを実行します。
```bash
python main.py

```


4. `converted_mp3/` フォルダを確認してください。

### 技術的な詳細

分割の閾値は以下の計算式に基づいています：

デフォルトでは **95MB** を上限としてマージンを確保しています。

---

### 次のステップ

もし「大量のファイルを一括で変換したい」といった要望や、Geminiへの「自動アップロード・文字起こしスクリプト」への統合が必要であれば、いつでもお伝えくださいね！