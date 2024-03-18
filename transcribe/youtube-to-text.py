import os
import argparse
from pytube import YouTube
from moviepy.editor import *
import openai
import json
import time


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--youtube_url", type=str, required=True, help='URL of the YouTube video')
    parser.add_argument("-d", "--download_dir", default=".", help='Path to download the video and audio')
    return parser.parse_args()


def get_api_key():
    api_key = os.environ.get('OPENAI_API_KEY')
    return api_key



def main():
    args = parse_args()
    openai.api_key = get_api_key()
    video_url = args.youtube_url
    download_path = args.download_dir

    # Create a YouTube object and get the highest resolution video stream
    yt = YouTube(video_url)
    youtube_video = yt.streams.get_lowest_resolution()
    # name and path without extension
    name = youtube_video.default_filename.rsplit('.', 1)[0]
    path = os.path.join(download_path, name) 

    # Download the video
    youtube_video.download(download_path)
    print(f'Downloaded: {name}')

    # Extract audio from the video
    video = VideoFileClip(path+".mp4")
    video.audio.write_audiofile(path+".mp3", fps=16000)
    print(f'Audio extracted: {name}\n Transcription in progress...')

    # Transcribe the audio to text
    audio_file= open(path+".mp3", "rb")
    start = time.time()
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    with open(path+".txt", "wt") as f:
        f.writelines(transcript["text"])
    print(f"Done! Transcription took {(time.time() - start):.1f}s.")


if __name__ == "__main__":
    main()