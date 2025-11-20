import io
import os
from dataclasses import dataclass

from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from PIL import Image


@dataclass
class Song:
    song_path: str
    cover_path: str | None
    title: str
    artist: str

    @property
    def full_name(self) -> str:
        return f"{self.title}\n{self.artist}"
    

def get_cover_img(mp3_file_path: str):
    audiofile = MP3(mp3_file_path, ID3=ID3)
    cover_img = None

    for tag in audiofile.tags.values():
        if tag.FrameID == "APIC":
            cover_img = Image.open(io.BytesIO(tag.data))
            break

    return cover_img



def parse_song_file(file_path: str) -> Song:
    title = "Неизвестная композиция"
    artist = "Неизвестный исполнитель"

    audiofile = MP3(file_path, ID3=ID3)

    if audiofile.tags:
        if "TIT2" in audiofile.tags:
            title = str(audiofile.tags["TIT2"])
        if "TPE1" in audiofile.tags:
            artist = str(audiofile.tags["TPE1"])

    return Song(
        song_path=file_path,
        cover_path=None,
        title=title,
        artist=artist
    )



def parse_songs_dir(dirpath: str) -> list[Song]:
    songs = []

    for filename in os.listdir(dirpath):
        if filename.endswith(".mp3"):
            path = os.path.join(dirpath, filename)
            song = parse_song_file(path)
            songs.append(song)
        
    return songs