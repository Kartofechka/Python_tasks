import customtkinter as ctk
import pygame
import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from PIL import Image
import io

from .utils import Song
from .app import App

current_index = 0
pause_mod = False



if __name__ == '__main__':
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    main_window = ctk.CTk()
    main_window.title("PotatoPlayer")

    screen_width = main_window.winfo_screenwidth()
    win_width = int(screen_width * 0.25)
    win_height = win_width * 5 / 4
    main_window.geometry(f"{win_width}x{win_height}")
    main_window.resizable(False, False)

    pygame.init()
    pygame.mixer.init()

    main_window.mainloop()

    app = App()
    app.run()
