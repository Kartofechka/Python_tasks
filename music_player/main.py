import customtkinter as ctk
import pygame
import os

from utils import Song, parse_songs_dir
from app import App

if __name__ == '__main__':
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    pygame.init()
    pygame.mixer.init()

    app = App(songs_dir_path="./music", default_cover_path="./assets/cover.jpg")
    app.run()