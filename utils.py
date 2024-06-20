import os
import json
import logging
import yt_dlp as youtube_dl
from pydub import AudioSegment

def create_folders(*folders):
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

def extract_metadata(url):
    ydl_opts = {
        'writeinfojson': False,
        'noplaylist': True,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(url, download=False)
    return meta

def save_metadata(meta, meta_file):
    meta_dict = {
        'title': meta['title'],
        'duration': meta['duration'],
        'tags': meta['tags'],
        'description': meta['description'],
    }
    with open(meta_file, 'w') as file:
        json.dump(meta_dict, file, ensure_ascii=False, indent=4)

def download_audio(url, audio_file, progress_hook=None):
    logging.getLogger('yt_dlp').setLevel(logging.ERROR)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': audio_file,
        'progress_hooks': [progress_hook] if progress_hook else [],
        'quiet': True,
        'no_warnings': True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def split_long_audio(video_id, audio_file, audio_dir, long_files_dir):
    try:
        print(audio_file)
        audio = AudioSegment.from_file(audio_file, format="mp3")
        duration_minutes = len(audio) // 60000
        os.makedirs(long_files_dir, exist_ok=True)
        os.rename(audio_file, os.path.join(long_files_dir, f"{video_id}.mp3"))

        for i in range(0, duration_minutes, 10):
            start_time = i * 60000
            end_time = (i + 10) * 60000
            split_audio = audio[start_time:end_time]
            split_audio_file = os.path.join(audio_dir, f"{video_id}_part_{i // 10 + 1}.mp3")
            split_audio.export(split_audio_file, format="mp3")

            progress = (i + 10) / duration_minutes * 100
            print(f"Split progress: {progress:.2f}%")

        print(f"Audio file for {video_id} has been split into {duration_minutes // 10} parts.")
    except Exception as e:
        print(f"Error splitting audio file for {video_id}: {str(e)}")
        raise