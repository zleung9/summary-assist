import os
import numpy as np
import time
import argparse

import whisper
model = whisper.load_model("base")

from pydub import AudioSegment
from pydub.utils import which
# https://github.com/jiaaro/pydub/issues/173
AudioSegment.converter = which("ffmpeg")


def read(k):
    y = np.array(k.get_array_of_samples())
    return np.float32(y) / 32768

def transcribe(path):
    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(path)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")

    # decode the audio
    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(model, mel, options)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--audio_file", default="audio.mp3")
    parser.add_argument("-t", "--text_file", default="text.txt")
    parser.add_argument("-l", "--language", default="english")
    args = parser.parse_args()
    
    suffix = args.audio_file.split(".")[-1]

    audio_name = args.audio_file
    text_name = args.text_file
    temp_path = "temp" + audio_name

    # Transcribe the audio to text
    sound = AudioSegment.from_file(audio_name, format=suffix)
    duration_ms = len(sound)
    n_segments = 4
    duration_per_segment_ms = int(np.ceil(duration_ms / n_segments))
    duration_per_segment_ms = 1000 * 60
    segments = sound[::duration_per_segment_ms]
    
    for i, segment in enumerate(segments):
        start = time.time()
        print(f"Started: Segment {i+1}/{n_segments}")
        file_handle = segment.export(temp_path, format="mp3")
        result = transcribe(temp_path)
        with open(text_name, "a") as f:
            f.write(f'\n{result.text}')
        end = time.time()
        print(f"Finished: Segment {i+1}/{n_segments}. Time: {int((end-start)/60)} min.")

if __name__ == "__main__":
    main()
# tr = read(audio[start:end])
# result = model.transcribe(tr, fp16=False)


# start = time.time()
# transcript = openai.Audio.transcribe("whisper-1", audio_file)
# with open(path+".txt", "wt") as f:
#     f.writelines(transcript["text"])
# print(f"Done! Transcription took {(time.time() - start):.1f}s.")
