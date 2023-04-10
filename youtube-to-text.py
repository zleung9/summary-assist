import os
import subprocess
from pytube import YouTube
from moviepy.editor import *
import speech_recognition as sr

# Replace the URL with the URL of the video you want to download
video_url = 'https://www.youtube.com/watch?v=GmShaplONDg'

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
recognizer = sr.Recognizer()


with sr.AudioFile(audio_path) as source:
    audio_data = recognizer.record(source)

try:
    # text = recognizer.recognize_google(audio_data)
    text = recognizer.recognize_sphinx(audio_data, language="zh-CN")
    print('Transcription:\n', text[:20])

    # Save transcription to a text file
    with open('transcription.txt', 'w') as f:
        f.write(text)

    print('Transcription saved to transcription.txt.')

except sr.UnknownValueError:
    print('Speech Recognition could not understand the audio.')
except sr.RequestError as e:
    print(f'Speech Recognition request failed: {e}')
