import os
import subprocess
from pytube import YouTube
from moviepy.editor import *
import openai
openai.api_key = "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"


# Replace the URL with the URL of the video you want to download
video_url = 'https://www.youtube.com/watch?v=8Xy8QBnt6yg'

# Create a YouTube object
yt = YouTube(video_url)

# Get the highest resolution video stream
video = yt.streams.get_highest_resolution()

# Set the download path (optional)
download_path = '/Users/zhuliang/Downloads'  # The current directory

# Download the video
video.download(download_path)

print(f'Video downloaded successfully: {video.default_filename}')

# Convert video to audio
video_path = os.path.join(download_path, video.default_filename)
audio_path = os.path.join(download_path, 'audio.wav')

subprocess.run(['ffmpeg', '-i', video_path, '-vn', '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1', audio_path])

print('Audio extracted successfully.')

# Transcribe the audio to text
audio_file= open("/Users/zhuliang/Downloads/audio.wav", "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file)
with open("transcription.txt", "wt") as f:
    f.writelines(transcript["text"])
    print("transcription finished!")
