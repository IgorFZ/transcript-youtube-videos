from moviepy.editor import VideoFileClip
import os
import math
import json
from pytube import YouTube
import speech_recognition as sr

def download_video_low_quality(youtube_url, output_dir):
    try:
        yt = YouTube(youtube_url)
        video_stream = yt.streams.filter(file_extension="mp4", resolution="360p").first()
        video_stream.download(filename="video.mp4", output_path=output_dir)
        video_title = yt.title
        return video_title
    except Exception as e:
        print(f"Error downloading video from {youtube_url}: {e}")
        return None

from moviepy.editor import VideoFileClip
import os

def split_audio(video_filepath, destination_dir, time_period=60):
    split_audio_map = {}
    count = 0

    video = VideoFileClip(video_filepath)

    audio = video.audio
    audio_filepath = os.path.join(destination_dir, "audio.wav")
    audio.write_audiofile(audio_filepath)

    duration = video.duration

    for i in range(0, math.ceil(duration), time_period):
        start = i
        end = min(i + time_period, duration)
        split_file = f"part_{start}_{end}.wav"

        audio_clip = audio.subclip(start, end)
        audio_clip_filepath = os.path.join(destination_dir, split_file)
        audio_clip.write_audiofile(audio_clip_filepath)

        split_audio_map[count] = split_file
        count += 1

    video.close()
    audio.close()

    return split_audio_map


def transcribe(split_audio, audio_splits_dir):
    recognizer = sr.Recognizer()

    with sr.AudioFile(os.path.join(audio_splits_dir, split_audio)) as source:
        audio_data = recognizer.record(source)

    try:
        transcript = recognizer.recognize_google(audio_data, show_all=False, language='pt-BR')
        return transcript
    except sr.UnknownValueError:
        return "Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from Google Web Speech API; {e}"


def main():
    output_dir = "tmp"
    data = []

    urls = [
        "https://www.youtube.com/watch?v=iU6mF107cAo",
        "https://www.youtube.com/watch?v=HSoNdY9sB8U",
        "https://www.youtube.com/watch?v=UAYq8G8pHkw",
        "https://www.youtube.com/watch?v=gx5CE_RqQXI&t",
        "https://www.youtube.com/watch?v=pqR0UxF2zBs",
        "https://www.youtube.com/watch?v=ZR2_OjGmvmk&t"
    ]

    for url in urls:
        video_title = download_video_low_quality(url, output_dir)
        print(f"Downloaded video: {video_title}")

        video_filepath = os.path.join(output_dir, "video.mp4")
        print(f"Downloaded video file: {video_filepath}")
        audio_splits_dir = os.path.join(output_dir, "audio_splits")
        os.makedirs(audio_splits_dir, exist_ok=True)

        split_audio_map = split_audio(video_filepath, audio_splits_dir, time_period=60)

        full_transcript = ""

        for index, split_audio_file in split_audio_map.items():
            transcript = transcribe(split_audio_file, audio_splits_dir)
            full_transcript += transcript + " "
            print(f"Transcribed audio {index}")

        video_info = {
            "title": video_title,
            "transcript": full_transcript
        }

        data.append(video_info)

    with open("teste.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        print("Data saved successfully.")

if __name__ == "__main__":
    main()
