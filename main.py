import argparse
from downloader import Downloader

def main(youtube_ids_file):
    downloader = Downloader(youtube_ids_file)
    downloader.download_data()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download audio and metadata from YouTube videos.')
    parser.add_argument('--youtube_ids_file', default='./dataset/Youtube_ytid.csv', type=str, help='Path to the file containing YouTube video IDs')
    args = parser.parse_args()
    
    main(args.youtube_ids_file)