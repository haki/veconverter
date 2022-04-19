import os

from pytube import YouTube
from datetime import datetime
import moviepy.editor as mpe


def on_progress_callback(chunk, file_handle, bytes_remaining):
    print(f"{round(((bytes_remaining / 1024) / 1024) / 1024, 2)} gb remaining")


def combine_audio_and_video(audio, video, name):
    location = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/media/"
    clip = mpe.VideoFileClip(video)
    audio_clip = mpe.AudioFileClip(audio)
    final_clip = clip.set_audio(audio_clip)
    final_clip.write_videofile(f'{location}{name.replace(".mp3", "")}.mp4')
    os.remove(video)
    os.remove(audio)

    return f"{name}.mp4"


class YoutubeService:
    def __init__(self, url):
        self.name = None
        self.location = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/media/"
        self.yt = YouTube(url, on_progress_callback=on_progress_callback)

    def convert_to_mp3(self):
        timestamp = datetime.timestamp(datetime.now())

        stream = self.yt.streams.filter(only_audio=True).first()
        output_file = stream.download(output_path=self.location)

        base, ext = os.path.splitext(output_file)
        new_file = f"{base.replace(' ', '_').lower()}_{timestamp}.mp3"
        os.rename(output_file, new_file)

        self.name = new_file.lower().replace(self.location.lower(), '')

        return self.name

    def get_resolutions(self):
        streams = []

        """
        StreamQueryHQ = self.yt.streams.order_by("resolution").desc()
        for k, s in enumerate(StreamQueryHQ):
            resolution = int(s.resolution.replace('p', ''))
            if resolution >= 1080 and s.codecs[0].find("vp9") != -1:
                streams.append(s)
        """

        StreamQueryLQ = self.yt.streams.filter(progressive=True).order_by("resolution").desc()
        for k, s in enumerate(StreamQueryLQ):
            streams.append(s)

        return streams

    def get_resolution_by_id(self, id):
        timestamp = datetime.timestamp(datetime.now())

        stream = self.yt.streams.get_by_itag(id)
        output_file = stream.download(output_path=self.location)
        base, ext = os.path.splitext(output_file)
        new_file = f"{base.replace(' ', '_').lower()}_{timestamp}{ext}"
        os.rename(output_file, new_file)
        self.name = new_file.lower().replace(self.location.lower(), '')

        resolution = int(stream.resolution.replace('p', ''))
        if resolution >= 1080:
            video_name = self.location + self.name
            audio_name = self.location + self.convert_to_mp3()

            combine = combine_audio_and_video(audio_name, video_name, self.name)
            self.name = combine.lower().replace(self.location.lower(), '')

        return self.name

    def get_thumbnail(self):
        thumbnail = self.yt.thumbnail_url
        return thumbnail

    def get_embed_url(self):
        embed_url = self.yt.embed_url
        return embed_url
