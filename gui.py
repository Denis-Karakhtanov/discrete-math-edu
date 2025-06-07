import tkinter as tk
from tkinter import ttk

class MainGUI:
    def __init__(self, app):
        """Инициализация GUI"""
        self.app = app
        self.main_frame = tk.Frame(self.app.root)
        self.main_frame.pack(fill="both", expand=True)
    
    def clear_frame(self):
        """Очистка главного фрейма"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()