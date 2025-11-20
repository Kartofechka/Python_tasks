import customtkinter as ctk
from PIL import Image
import pygame

from .utils import parse_songs_dir, get_cover_img



class App:

    def __init__(
            self,
            songs_dir_path: str,
            default_cover_path: str
    ):
        self._default_cover_path = default_cover_path

        self._main_window = ctk.CTk()
        self._songs = parse_songs_dir(songs_dir_path)
        self._curr_idx = 0


    def clear_window(self):
        for widget in self._main_window.winfo_children():
            widget.destroy()


    def output_music_info(self):
        text = None

        if self._songs:
            current_song = self._songs[self._curr_idx]
            text = current_song.full_name

            cover_img = None
            if current_song.cover_path is not None:
                cover_img = Image.open(current_song.cover_path)
            else:
                cover_img = get_cover_img(current_song.song_path)
            if not cover_img:
                cover_img = Image.open(self._default_cover_path)

            cover_ctk = ctk.CTkImage(cover_img, size=(250, 250))
            cover_label = ctk.CTkLabel(self._main_window, image=cover_ctk, text="")
            cover_label.pack(pady=20)
        else:
            text = "Нет музыки в папке"

        label = ctk.CTkLabel(self._main_window, text=text, font=("Arial", 20))
        label.pack(pady=20)


    def give_operate_buttons(self):
        button_frame = ctk.CTkFrame(self._main_window, fg_color="transparent")
        button_frame.pack(pady=20)

        menu_button = ctk.CTkButton(
            button_frame, 
            text="☰", 
            width=30, 
            height=30,
            corner_radius=15, 
            font=("Arial", 30), 
            fg_color="transparent"
        )
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
        main_window.attributes("-alpha", value)



    def slider_settings(text, from_, command, set_value):
        frame = ctk.CTkFrame(main_window, fg_color="transparent")
        frame.pack(pady=10)

        label = ctk.CTkLabel(frame, text=text, font=("Arial", 30))
        label.pack(side="left", padx=5)

        slider = ctk.CTkSlider(frame, from_=from_, to=1, command=command)
        slider.set(set_value)
        slider.pack(pady=10)
        
        

    def run(self):
        self.clear_window()
        self.output_music_info()

        progressbar = ctk.CTkProgressBar(self._main_window, orientation="horizontal")
        progressbar.pack(pady=10)

        self.give_operate_buttons()
        slider_settings(text='🕪', from_=0, command=set_volume, set_value=0.5)
        slider_settings(text='🌓', from_=0.3, command=set_opacity, set_value=1)