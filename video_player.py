import tkinter as tk
from tkinter import filedialog, messagebox
import vlc
import os

class VideoPlayer:
    def __init__(self, root, video_path=None):
        self.root = root
        self.video_path = video_path
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.media = None

        # Создание фрейма для видео
        self.video_frame = tk.Frame(self.root)
        self.video_frame.pack(fill=tk.BOTH, expand=True)

        # Создание области для воспроизведения видео
        self.canvas = tk.Canvas(self.video_frame, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Панель управления
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(fill=tk.X)

        # Кнопки управления
        tk.Button(self.control_frame, text="Открыть", command=self.open_file).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Воспроизвести", command=self.play_video).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Пауза", command=self.pause_video).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Стоп", command=self.stop_video).pack(side=tk.LEFT, padx=5)

        # Привязка видео к canvas (для Windows)
        if os.name == "nt":
            self.player.set_hwnd(self.canvas.winfo_id())
        else:
            self.player.set_xwindow(self.canvas.winfo_id())

        if self.video_path:
            self.load_video(self.video_path)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mkv")])
        if file_path:
            self.load_video(file_path)

    def load_video(self, file_path):
        if not os.path.exists(file_path):
            messagebox.showerror("Ошибка", "Файл не найден!")
            return
        self.media = self.instance.media_new(file_path)  # Строка 47
        self.player.set_media(self.media)  # Строка 48
        self.play_video()

    def play_video(self):
        if self.player:
            self.player.play()

    def pause_video(self):
        if self.player:
            self.player.pause()

    def stop_video(self):
        if self.player:
            self.player.stop()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Проигрыватель видео")
    root.geometry("800x600")
    player = VideoPlayer(root)
    root.mainloop()