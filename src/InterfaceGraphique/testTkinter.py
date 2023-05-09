import tkinter
import customtkinter as ctk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import os



ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


app = ctk.CTk()


label = ctk.CTkLabel(app)
label.destroy()
print(type(label))
label.destroy()

