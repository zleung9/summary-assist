import os
from pytube import YouTube
from moviepy.editor import *
import openai
import json
import time

with open('config.json', 'r') as json_file:
    config = json.load(json_file)

openai.api_key = config["api_key"]
video_url = config["youtube_url"]
download_path = config["download_path"]

# Create a YouTube object and get the highest resolution video stream
yt = YouTube(video_url)
youtube_video = yt.streams.get_highest_resolution()
# name and path without extension
name = youtube_video.default_filename.rsplit('.', 1)[0]
path = os.path.join(download_path, name) 

# Download the video
youtube_video.download(download_path)
print(f'Video downloaded successfully: {name}')

# Extract audio from the video
video = VideoFileClip(path+".mp4")
video.audio.write_audiofile(path+".mp3", fps=16000)
print('Audio extracted successfully.')

# Transcribe the audio to text
audio_file= open(path+".mp3", "rb")
start = time.time()
transcript = openai.Audio.transcribe("whisper-1", audio_file)
with open(path+".txt", "wt") as f:
    f.writelines(transcript["text"])
print(f"Done! Transcription took {(time.time() - start):.1f}s.")
