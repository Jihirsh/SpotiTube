import tkinter as tk
from tkinter import messagebox
import webbrowser
from convert import convert_playlist

def convert():
    spotify_url = entry.get().strip()
    if not spotify_url:
        messagebox.showerror("Error", "Please enter a Spotify playlist URL.")
        return
    
    result_label.config(text="Converting...", fg="white")
    try:
        yt_music_link = convert_playlist(spotify_url)
        if yt_music_link:
            result_label.config(text=f"Converted! Click below:", fg="#00A2FF")
            link_button.config(text=yt_music_link, fg="#00A2FF", cursor="hand2")
            link_button.bind("<Button-1>", lambda e: webbrowser.open(yt_music_link))
        else:
            result_label.config(text="Conversion failed.", fg="red")
    except Exception as e:
        messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("SpotiTube - Spotify to YouTube Music Converter")
root.geometry("500x300")
root.configure(bg="#0A0A0A")


title_label = tk.Label(root, text="SpotiTube", font=("Arial", 20, "bold"), fg="#00A2FF", bg="#0A0A0A")
title_label.pack(pady=10)

desc_label = tk.Label(root, text="Convert Spotify Playlists to YouTube Music", font=("Arial", 12), fg="white", bg="#0A0A0A")
desc_label.pack()

entry = tk.Entry(root, width=50, font=("Arial", 12), bg="#1E1E2E", fg="white", insertbackground="white")
entry.pack(pady=10)

convert_button = tk.Button(root, text="Convert Playlist", font=("Arial", 12, "bold"), bg="#007BFF", fg="white", command=convert)
convert_button.pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 12), fg="white", bg="#0A0A0A")
result_label.pack()

link_button = tk.Label(root, text="", font=("Arial", 12, "underline"), fg="#0A0A0A", bg="#0A0A0A")
link_button.pack()

root.mainloop()
