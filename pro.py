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
    bitrate_int = int(bitrate.replace("k", "")) * 1000
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
