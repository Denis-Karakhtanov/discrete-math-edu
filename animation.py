import tkinter as tk
import random
import time

class AnimationManager:
    def __init__(self, app):
        """Инициализация менеджера анимаций"""
        self.app = app
        self.canvas = None
    
    def animate_graph(self):
        """Анимация построения графа"""
        window = tk.Toplevel()
        window.title("Анимация графа")
        window.geometry("600x600")
        self.canvas = tk.Canvas(window, width=600, height=600, bg="white")
        self.canvas.pack()
        
        vertices = [(100, 100), (200, 100), (150, 200), (250, 200), (200, 300)]
        vertex_ids = []
        for x, y in vertices:
            vertex_id = self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="blue")
            vertex_ids.append(vertex_id)
        
        edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
        for i, (v1, v2) in enumerate(edges):
            self.canvas.after(1000 * (i + 1), lambda v1=v1, v2=v2: self.draw_edge(vertices[v1], vertices[v2]))
        self.app.logger.log("Запущена анимация графа")
    
    def animate_set(self):
        """Анимация множества"""
        window = tk.Toplevel()
        window.title("Анимация множества")
        window.geometry("600x600")
        self.canvas = tk.Canvas(window, width=600, height=600, bg="white")
        self.canvas.pack()
        
        set_a = [(200, 200, "A1"), (250, 200, "A2"), (200, 250, "A3")]
        set_b = [(350, 200, "B1"), (400, 200, "B2"), (350, 250, "B3")]
        
        self.canvas.create_oval(150, 150, 300, 300, outline="blue", width=2)
        self.canvas.create_text(150, 150, text="A", font=("Arial", 12))
        self.canvas.create_oval(300, 150, 450, 300, outline="red", width=2)
        self.canvas.create_text(450, 150, text="B", font=("Arial", 12))
        
        for i, (x, y, label) in enumerate(set_a):
            self.canvas.after(1000 * (i + 1), lambda x=x, y=y, label=label: self.draw_element(x, y, label, "blue"))
        for i, (x, y, label) in enumerate(set_b):
            self.canvas.after(1000 * (i + 4), lambda x=x, y=y, label=label: self.draw_element(x, y, label, "red"))
        self.app.logger.log("Запущена анимация множества")
    
    def animate_logic(self):
        """Анимация логической операции"""
        window = tk.Toplevel()
        window.title("Анимация логики")
        window.geometry("600x600")
        self.canvas = tk.Canvas(window, width=600, height=600, bg="white")
        self.canvas.pack()
        
        self.canvas.create_text(300, 100, text="A AND B", font=("Arial", 16))
        self.canvas.create_rectangle(200, 200, 250, 250, fill="gray")
        self.canvas.create_text(225, 225, text="A=0", font=("Arial", 12))
        self.canvas.create_rectangle(350, 200, 400, 250, fill="gray")
        self.canvas.create_text(375, 225, text="B=0", font=("Arial", 12))
        
        for i in range(4):
            a = i % 2
            b = (i // 2) % 2
            result = a and b
            self.canvas.after(1000 * (i + 1), lambda a=a, b=b, result=result: self.update_logic(a, b, result))
        self.app.logger.log("Запущена анимация логики")
    
    def draw_edge(self, v1, v2):
        """Рисование ребра"""
        self.canvas.create_line(v1[0], v1[1], v2[0], v2[1], fill="black", width=3)
    
    def draw_element(self, x, y, label, color):
        """Рисование элемента множества"""
        self.canvas.create_oval(x-10, y-10, x+10, y+10, fill=color)
        self.canvas.create_text(x, y, text=label, font=("Arial", 10))
    
    def update_logic(self, a, b, result):
        """Обновление логической анимации"""
        self.canvas.delete("logic")
        self.canvas.create_text(225, 225, text=f"A={a}", font=("Arial", 12), tags="logic")
        self.canvas.create_text(375, 225, text=f"B={b}", font=("Arial", 12), tags="logic")
        self.canvas.create_text(300, 300, text=f"Результат: {result}", font=("Arial", 14), tags="logic")