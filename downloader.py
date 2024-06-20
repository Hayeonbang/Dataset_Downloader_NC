import os
import json
import yt_dlp as youtube_dl
from utils import create_folders, extract_metadata, save_metadata, download_audio, split_long_audio

class Downloader:
    def __init__(self, youtube_ids_file):
        self.youtube_ids_file = youtube_ids_file
        self.base_dir = os.path.dirname(youtube_ids_file)
        self.data_dir = os.path.join('./','Youtube_Dataset')
        self.audio_dir = os.path.join(self.data_dir, 'audio')
        self.meta_dir = os.path.join(self.data_dir, 'meta')
        self.long_files_dir = os.path.join(self.data_dir, 'long_files')

    def download_data(self):
        create_folders(self.audio_dir, self.meta_dir, self.long_files_dir)
        self._download_audio_and_metadata()

    def _download_audio_and_metadata(self):
        with open(self.youtube_ids_file, 'r') as file:
            youtube_ids = [line.strip() for line in file]

        for i, video_id in enumerate(youtube_ids, start=1):
            print(f"Processing video {i}/{len(youtube_ids)}: {video_id}")
            self._process_video(video_id)

    def _process_video(self, video_id):
        url = f"https://www.youtube.com/watch?v={video_id}"
        filename = os.path.join(self.audio_dir, f"{video_id}")
        audio_file = os.path.join(self.audio_dir, f"{video_id}.mp3")
        long_audio_file = os.path.join(self.long_files_dir, f"{video_id}.mp3")
        meta_file = os.path.join(self.meta_dir, f"{video_id}.json")

        if os.path.isfile(meta_file) and (os.path.isfile(audio_file) or os.path.isfile(long_audio_file)):
            print(f"Metadata and audio files for {video_id} already exist. Skipping...")
            return

        try:
            meta = extract_metadata(url)
            duration_seconds = meta['duration']
            duration_minutes = duration_seconds // 60

            if not os.path.isfile(meta_file):
                save_metadata(meta, meta_file)
                print(f"Metadata for {video_id} saved successfully.")
                
            if not os.path.isfile(audio_file) and not os.path.isfile(long_audio_file):
                def progress_hook(progress):
                    percent = progress['downloaded_bytes'] / progress['total_bytes'] * 100
                    if percent >= 50 and not hasattr(progress_hook, 'fifty_percent_shown'):
                        print(f"Download progress: {percent:.2f}%")
                        progress_hook.fifty_percent_shown = True
                    elif percent >= 100 and not hasattr(progress_hook, 'hundred_percent_shown'):
                        print(f"Download progress: {percent:.2f}%")
                        progress_hook.hundred_percent_shown = True
            
                download_audio(url, filename, progress_hook)

                if duration_minutes >= 30:
                    print(f"Audio file for {video_id} is longer than 30 minutes. Splitting into 10-minute parts...")
                    split_long_audio(video_id, audio_file, self.audio_dir, self.long_files_dir)
                else:
                    print(f"Audio file for {video_id} is less than 30 minutes. No splitting required.")

                print(f"Audio for {video_id} processed successfully.")
            else:
                print(f"Audio file for {video_id} already exists. Skipping download.")

            print(f"Processing for {video_id} completed.")
        except Exception as e:
            print(f"Error processing {video_id}: {str(e)}")