import customtkinter as ctk
import pygame
import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from PIL import Image
import io

from .utils import Song

current_index = 0
pause_mod = False


def parse_song(file_path: str) -> Song:
    title = "Неизвестная композиция"
    artist = "Неизвестный исполнитель"
    cover_img = None

    audiofile = MP3(file_path, ID3=ID3)

    if audiofile.tags:
        if "TIT2" in audiofile.tags:
            title = str(audiofile.tags["TIT2"])
        if "TPE1" in audiofile.tags:
            artist = str(audiofile.tags["TPE1"])
        for tag in audiofile.tags.values():
            if tag.FrameID == "APIC":
                cover_img = Image.open(io.BytesIO(tag.data))
                break

    return Song(
        song_path=file_path,
        cover_path=None,
        title=title,
        artist=artist
    )



def get_all_music(dirpath: str) -> list[Song]:
    songs = []

    for filename in os.listdir(dirpath):

        if not filename.endswith(".mp3"):
            continue

        path = os.path.join(dirpath, filename)
        audiofile = MP3(path, ID3=ID3)

        title = "Неизвестная композиция"
        artist = "Неизвестный исполнитель"
        cover_img = None

        if audiofile.tags:
            if "TIT2" in audiofile.tags:
                title = str(audiofile.tags["TIT2"])
            if "TPE1" in audiofile.tags:
                artist = str(audiofile.tags["TPE1"])
            for tag in audiofile.tags.values():
                if tag.FrameID == "APIC":
                    cover_img = Image.open(io.BytesIO(tag.data))
                    break

        songs.append(
            Song(
                song_path=path,
                cover_path=None,
                title=title,
                artist=artist
            )
        )

    return songs

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


def output_music_info():
    global current_index
    if songs:
        current_song = songs[current_index]
        text = f"{current_song['title']}\n{current_song['artist']}"

        if current_song["cover"]:
            cover_ctk = ctk.CTkImage(current_song["cover"], size=(250, 250))
            cover_label = ctk.CTkLabel(root, image=cover_ctk, text="")
            cover_label.pack(pady=20)
        else:
            cover_ctk = ctk.CTkImage(Image.open("assets/cover.jpg"), size=(250, 250))
            cover_label = ctk.CTkLabel(root, image=cover_ctk, text="")
            cover_label.pack(pady=20)
    else:
        text = "Нет музыки в папке"

    label = ctk.CTkLabel(root, text=text, font=("Arial", 20))
    label.pack(pady=20)


def give_operate_buttons():
    button_frame = ctk.CTkFrame(root, fg_color="transparent")
    button_frame.pack(pady=20)

    menu_button = ctk.CTkButton(button_frame, text="☰", width=30, height=30,
                                corner_radius=15, font=("Arial", 30), fg_color="transparent")
    menu_button.pack(side="left", padx=10)

    prewies_button = ctk.CTkButton(button_frame, text="⏮", width=30, height=30,
                                   corner_radius=15, font=("Arial", 30),
                                   fg_color="transparent", command=prev_song)
    prewies_button.pack(side="left", padx=10)

    play_button = ctk.CTkButton(button_frame, text="⏵", width=30, height=30,
                                corner_radius=15, font=("Arial", 30),
                                fg_color="transparent", command=play_song(current_index))
    play_button.pack(side="left", padx=10)

    next_button = ctk.CTkButton(button_frame, text="⏭", width=30, height=30,
                                corner_radius=15, font=("Arial", 30),
                                fg_color="transparent", command=next_song)
    next_button.pack(side="left", padx=10)

    nail_button = ctk.CTkButton(button_frame, text="📌", width=30, height=30,
                                corner_radius=15, font=("Arial", 30), fg_color="transparent")
    nail_button.pack(side="left", padx=10)



def play_song(index):
    global pause_mod
    global current_index
    if pause_mod == False:
        play_button.configure(text="⏸")
        pause_mod = True
    else:
        play_button.configure(text="⏭")
        pause_mod = False
    if 0 <= index < len(songs):
        current_index = index
        current_song = songs[current_index]

        pygame.mixer.music.load(current_song["file"])
        pygame.mixer.music.play()

        firstMenu()


def next_song():
    global current_index
    if songs:
        new_index = (current_index + 1) % len(songs)
        play_song(new_index)


def prev_song():
    global current_index
    if songs:
        new_index = (current_index - 1) % len(songs)
        play_song(new_index)


def set_volume(value):
    pygame.mixer.music.set_volume(value)


def set_opacity(value):
    root.attributes("-alpha", value)


def firstMenu():
    clear_window()
    output_music_info()

    progressbar = ctk.CTkProgressBar(root, orientation="horizontal")
    progressbar.pack(pady=10)

    give_operate_buttons()
    slider_settings(text='🕪', from_=0, command=set_volume, set_value=0.5)
    slider_settings(text='🌓', from_=0.3, command=set_opacity, set_value=1)


def slider_settings(text, from_, command, set_value):
    frame = ctk.CTkFrame(root, fg_color="transparent")
    frame.pack(pady=10)

    label = ctk.CTkLabel(frame, text=text, font=("Arial", 30))
    label.pack(side="left", padx=5)

    slider = ctk.CTkSlider(frame, from_=from_, to=1, command=command)
    slider.set(set_value)
    slider.pack(pady=10)


if __name__ == '__main__':
    root = ctk.CTk()
    root.title("PotatoPlayer")
    
    screen_width = root.winfo_screenwidth()
    win_width = int(screen_width * 0.25)
    win_height = win_width * 5 / 4
    root.geometry(f"{win_width}x{win_height}")
    root.resizable(False, False)

    pygame.init()
    pygame.mixer.init()

    get_all_music()
    firstMenu()

    root.mainloop()
