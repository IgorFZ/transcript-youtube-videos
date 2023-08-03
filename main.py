import speech_recognition as sr
from pytube import YouTube
import json
from moviepy.editor import *

def download_video_low_quality(youtube_url):
    try:
        yt = YouTube(youtube_url)
        video_stream = yt.streams.filter(file_extension="mp4", resolution="360p").first()
        video_stream.download(filename="video.mp4")
        video_title = yt.title
        return video_title
    except Exception as e:
        print(f"Error downloading video from {youtube_url}: {e}")
        return None

video_urls = [
    "https://youtu.be/5DU5jkHSXhw",
    "https://youtu.be/SkReQdVjTFY",
    "https://youtu.be/LQheerKgTlw",
    "https://youtu.be/T-DtLcSv7Ds",
    "https://youtu.be/dJJd7jAwzEQ",
    "https://youtu.be/eZeKYnnBVL4",
    "https://youtu.be/_sPX8zUXgGk",
    "https://youtube.com/shorts/z3wc-cxTSSk",
    "https://youtube.com/shorts/4f5szgCg8wE",
    "https://youtu.be/mnIQSEdZloU",
    "https://youtu.be/euCwf8IbLvA",
    "https://www.youtube.com/watch?v=8NkX-lpdUUc&t",
    "https://www.youtube.com/watch?v=rujhK5ddP_A&t",
    "https://www.youtube.com/watch?v=ftv9hUvESsc&t",
    "https://www.youtube.com/watch?v=pOCKCSrVgnk",
    "https://www.youtube.com/watch?v=eJ58Oc62Cto",
    "https://www.youtube.com/watch?v=afl_T6zClUo",
]

r = sr.Recognizer()
data = []

for url in video_urls:
    try:
        video_title = download_video_low_quality(url)

        video = VideoFileClip("video.mp4")
        audio = video.audio
        audio.write_audiofile("audio.wav")

        with sr.AudioFile("audio.wav") as source:
            audio_text = r.record(source)
        text = r.recognize_google(audio_text, language='pt-BR')

        video_info = {
            "title": video_title,
            "transcript": text
        }

        data.append(video_info)

        print(f"Video from {url} downloaded and transcribed successfully.")
    except Exception as e:
        print(f"Error processing video from {url}: {e}")

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    print("Data saved successfully.")