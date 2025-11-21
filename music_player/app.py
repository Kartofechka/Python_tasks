import customtkinter as ctk
from PIL import Image
import pygame
from mutagen.mp3 import MP3
import time

from utils import parse_songs_dir, get_cover_img


class App:
    def __init__(self, songs_dir_path: str, default_cover_path: str):
        self._default_cover_path = default_cover_path
        self._main_window = ctk.CTk()
        self._main_window.title("PotatoPlayer")
        self._main_window.iconbitmap("./assets/favicon.ico")
        screen_width = self._main_window.winfo_screenwidth()
        win_width = int(screen_width * 0.25)
        win_height = int(win_width * 5 / 4)
        self._main_window.geometry(f"{win_width}x{win_height}")
        self._main_window.resizable(False, False)
        self._songs = parse_songs_dir(songs_dir_path)
        self._curr_idx = 0
        self.pause_mod = True
        self.topmost = False
        self.seek_offset = 0
        self.icons = {
            "play": ctk.CTkImage(Image.open("./assets/play.png"), size=(40, 40)),
            "pause": ctk.CTkImage(Image.open("./assets/pause.png"), size=(40, 40)),
            "next": ctk.CTkImage(Image.open("./assets/next.png"), size=(40, 40)),
            "prev": ctk.CTkImage(Image.open("./assets/prev.png"), size=(40, 40)),
            "menu": ctk.CTkImage(Image.open("./assets/menu.png"), size=(40, 40)),
        }
        self.create_interface()
        self.update_song_info()

    def clear_window(self):
        for widget in self.info_frame.winfo_children():
            widget.destroy()

    def output_music_info(self):
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
            cover_label = ctk.CTkLabel(self.info_frame, image=cover_ctk, text="")
            cover_label.pack(pady=20)
        else:
            text = "Нет музыки в папке"
        label = ctk.CTkLabel(self.info_frame, text=text, font=("Arial", 20))
        label.pack(pady=20)

    def give_operate_buttons(self):
        button_frame = ctk.CTkFrame(self._main_window, fg_color="transparent")
        button_frame.pack(pady=20)

        ctk.CTkButton(
            button_frame,
            image=self.icons["menu"],
            text="",
            width=40,
            height=40,
            fg_color="transparent",
            hover=False,
            command=self.get_all_music_menu
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            button_frame,
            image=self.icons["prev"],
            text="",
            width=40,
            height=40,
            fg_color="transparent",
            hover=False,
            command=self.prev_song
        ).pack(side="left", padx=10)

        self.play_button = ctk.CTkButton(
            button_frame,
            image=self.icons["play"],
            text="",
            width=40,
            height=40,
            fg_color="transparent",
            hover=False,
            command=self.toggle_play
        )
        self.play_button.pack(side="left", padx=10)

        ctk.CTkButton(
            button_frame,
            image=self.icons["next"],
            text="",
            width=40,
            height=40,
            fg_color="transparent",
            hover=False,
            command=self.next_song
        ).pack(side="left", padx=10)

        self.nail_button = ctk.CTkButton(
            button_frame,
            text="📌",
            width=40,
            height=40,
            fg_color="transparent",
            hover=False,
            command=self.toggle_topmost
        )
        self.nail_button.pack(side="left", padx=10)


    def toggle_topmost(self):
        self.topmost = not self.topmost
        self._main_window.attributes("-topmost", self.topmost)
        if self.topmost:
            self.nail_button.configure(fg_color="#0E5221")
        else:
            self.nail_button.configure(fg_color="transparent")

    def play_song(self, index):
        if 0 <= index < len(self._songs):
            self._curr_idx = index
            current_song = self._songs[self._curr_idx]
            pygame.mixer.music.load(current_song.song_path)
            pygame.mixer.music.play()
            self.play_button.configure(image=self.icons["pause"])
            self.pause_mod = False

            self.seek_offset = 0

            audio = MP3(current_song.song_path)
            self.track_length = int(audio.info.length)
            self.progress_slider.configure(to=self.track_length)
            self.update_song_info()


    def toggle_play(self):
        if not self._songs:
            return
        if pygame.mixer.music.get_busy() and not self.pause_mod:
            pygame.mixer.music.pause()
            self.play_button.configure(image=self.icons["play"])
            self.pause_mod = True
        else:
            self.play_song(self._curr_idx)


    def next_song(self):
        if self._songs:
            new_index = (self._curr_idx + 1) % len(self._songs)
            self.play_song(new_index)

    def prev_song(self):
        if self._songs:
            new_index = (self._curr_idx - 1) % len(self._songs)
            self.play_song(new_index)

    def set_volume(self, value):
        pygame.mixer.music.set_volume(value)

    def slider_settings(self, text, from_, command, set_value):
        frame = ctk.CTkFrame(self._main_window, fg_color="transparent")
        frame.pack(pady=10)
        ctk.CTkLabel(frame, text=text, font=("Arial", 30)).pack(side="left", padx=5)
        slider = ctk.CTkSlider(frame, from_=from_, to=1, command=command)
        slider.set(set_value)
        slider.pack(pady=10)
        return slider

    def get_all_music_menu(self):
        self.music_menu = MusicMenu(self)
        self.music_menu.run()

    def get_settings_menu(self):
        settings_menu = SettingsMenu(self)
        settings_menu.run()

    def create_interface(self):
        self.settings_button = ctk.CTkButton(
            self._main_window,
            text="☭",
            width=40,
            height=40,
            corner_radius=20,
            font=("Arial", 25),
            fg_color="transparent",
            hover=False,
            command=self.get_settings_menu
        )

        self.settings_button.place(relx=1.0, rely=0.0, anchor="ne")

        self.info_frame = ctk.CTkFrame(self._main_window, fg_color="transparent")
        self.info_frame.pack(pady=10)
        self.progress_slider = ctk.CTkSlider(self._main_window, width=300, from_=0, to=100, command=self.seek_song)
        self.progress_slider.pack(pady=10, fill="x")
        self.progress_slider.place(relx=0.5, rely=0.62, anchor="center")

        self.time_label = ctk.CTkLabel(self._main_window, text="0:00 / 0:00", font=("Arial", 15))
        self.time_label.pack()

        self.give_operate_buttons()
        self.volume_slider = self.slider_settings(text='🕪', from_=0, command=self.set_volume, set_value=0.5)

        self.update_progress()

    def update_progress(self):
        if pygame.mixer.music.get_busy():
            pos_ms = pygame.mixer.music.get_pos()
            if pos_ms >= 0:
                pos_sec = pos_ms // 1000 + self.seek_offset
                self.progress_slider.set(pos_sec)
                self.time_label.configure(
                    text=f"{time.strftime('%M:%S', time.gmtime(pos_sec))} / {time.strftime('%M:%S', time.gmtime(self.track_length))}"
                )
        self._main_window.after(500, self.update_progress)


    def seek_song(self, value):
        self.seek_offset = int(value)
        pygame.mixer.music.play(start=self.seek_offset)


    def update_song_info(self):
        self.clear_window()
        self.output_music_info()


    def run(self):
        self._main_window.mainloop()


class MusicMenu:
    def __init__(self, app: App):
        self.app = app
        self._main_window = ctk.CTkToplevel(app._main_window)
        self._main_window.title("PotatoPlayer/AllMusic")
        self._main_window.iconbitmap("./assets/favicon.ico")

        screen_width = self._main_window.winfo_screenwidth()
        menu_width = int(screen_width * 0.25)
        menu_height = int(menu_width * 5 / 4)

        x = app._main_window.winfo_x()
        y = app._main_window.winfo_y()
        self._main_window.geometry(f"{menu_width}x{menu_height}+{x - menu_width}+{y}")
        self._main_window.resizable(False, False)

        scroll_frame = ctk.CTkScrollableFrame(self._main_window, width=menu_width-20, height=menu_height-20)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        header_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(header_frame, text="Название", font=("Arial", 16, "bold"), anchor="w").pack(side="left", padx=10, fill="x", expand=True)
        ctk.CTkLabel(header_frame, text="Автор", font=("Arial", 16, "bold"), anchor="w").pack(side="left", padx=10, fill="x", expand=True)

        if app._songs:
            for idx, song in enumerate(app._songs):
                row = ctk.CTkFrame(scroll_frame, fg_color="transparent")
                row.pack(fill="x", pady=2)

                ctk.CTkLabel(row, text=song.title, anchor="w", font=("Arial", 14)).pack(side="left", padx=10, fill="x", expand=True)

                ctk.CTkLabel(row, text=song.artist, anchor="w", font=("Arial", 14)).pack(side="left", padx=10, fill="x", expand=True)

                play_btn = ctk.CTkButton(
                    row,
                    image=self.app.icons["play"],
                    text="",
                    width=30,
                    height=30,
                    fg_color="transparent",
                    hover=False,
                    command=lambda i=idx: app.play_song(i)
                )
                play_btn.pack(side="right", padx=5)

        else:
            ctk.CTkLabel(scroll_frame, text="Нет музыки в папке").pack(pady=10)

    def run(self):
        self._main_window.mainloop()



class SettingsMenu:
    def __init__(self, app: App):
        self.app = app
        self._main_window = ctk.CTk()
        self._main_window.title("PotatoPlayer/Settings")
        self._main_window.iconbitmap("./assets/favicon.ico")

        screen_width = self._main_window.winfo_screenwidth()
        settings_width = int(screen_width * 0.2)
        settings_height = int(settings_width * 2 / 8)

        x = app._main_window.winfo_x()
        y = app._main_window.winfo_y()
        w = app._main_window.winfo_width()
        self._main_window.geometry(f"{settings_width}x{settings_height}+{x + w}+{y}")
        self._main_window.resizable(False, False)

        self.opacity_slider = self.slider_settings(
            text='🌓',
            from_=0.3,
            command=self.set_opacity,
            set_value=1
        )

    def set_opacity(self, value):
        self.app._main_window.attributes("-alpha", value)
        self.app.music_menu._main_window.attributes("-alpha", value)    


    def slider_settings(self, text, from_, command, set_value):
        frame = ctk.CTkFrame(self._main_window, fg_color="transparent")
        frame.pack(pady=10)
        ctk.CTkLabel(frame, text=text, font=("Arial", 30)).pack(side="left", padx=5)
        slider = ctk.CTkSlider(frame, from_=from_, to=1, command=command)
        slider.set(set_value)
        slider.pack(pady=10)
        return slider

    def run(self):
        self._main_window.mainloop()