import tkinter as tk
import math

class AnimationManager:
    def __init__(self, logger):
        self.logger = logger
        self.canvas = None

    def animate_graph(self):
        window = tk.Toplevel()
        window.title("Анимация графа")
        window.geometry("600x600")
        self.canvas = tk.Canvas(window, width=600, height=600, bg="white")
        self.canvas.pack()

        vertices = [(100, 100), (200, 100), (150, 200), (250, 200), (200, 300)]
        vertex_ids = []
        for x, y in vertices:
            vertex_id = self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="blue")
            vertex_ids.append(vertex_id)

        edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
        for i, (v1, v2) in enumerate(edges):
            self.canvas.after(1000 * (i + 1), lambda v1=v1, v2=v2: self.draw_edge(vertices[v1], vertices[v2]))
        self.logger.log("Запущена анимация графа")

    def animate_set(self):
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
        self.logger.log("Запущена анимация множества")

    def animate_logic(self):
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
        self.logger.log("Запущена анимация логики")

    def animate_circle_graph(self):
        window = tk.Toplevel()
        window.title("Круговой граф")
        window.geometry("600x600")
        self.canvas = tk.Canvas(window, width=600, height=600, bg="white")
        self.canvas.pack()

        radius = 200
        center_x = 300
        center_y = 300
        node_count = 6
        angle_step = 360 / node_count
        angle_offset = 0
        nodes = []
        lines = []

        for i in range(node_count):
            angle = math.radians(i * angle_step)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            node = self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="green")
            nodes.append(node)

        for i in range(node_count):
            a = i
            b = (i + 1) % node_count
            x1_bbox, y1_bbox, x2_bbox, y2_bbox = self.canvas.coords(nodes[a])
            x1_center = (x1_bbox + x2_bbox) / 2
            y1_center = (y1_bbox + y2_bbox) / 2

            x3_bbox, y3_bbox, x4_bbox, y4_bbox = self.canvas.coords(nodes[b])
            x2_center = (x3_bbox + x4_bbox) / 2
            y2_center = (y3_bbox + y4_bbox) / 2

            line = self.canvas.create_line(x1_center, y1_center, x2_center, y2_center, fill="gray", width=2)
            lines.append(line)

        def update_loop():
            nonlocal angle_offset
            angle_offset = (angle_offset + 2) % 360

            for i in range(node_count):
                angle = math.radians(i * angle_step + angle_offset)
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                self.canvas.coords(nodes[i], x - 10, y - 10, x + 10, y + 10)

            for idx, (a, b) in enumerate([(i, (i + 1) % node_count) for i in range(node_count)]):
                x1_bbox, y1_bbox, x2_bbox, y2_bbox = self.canvas.coords(nodes[a])
                x1_center = (x1_bbox + x2_bbox) / 2
                y1_center = (y1_bbox + y2_bbox) / 2

                x3_bbox, y3_bbox, x4_bbox, y4_bbox = self.canvas.coords(nodes[b])
                x2_center = (x3_bbox + x4_bbox) / 2
                y2_center = (y3_bbox + y4_bbox) / 2

                self.canvas.coords(lines[idx], x1_center, y1_center, x2_center, y2_center)

            self.canvas.after(50, update_loop)

        update_loop()
        self.logger.log("Запущена круговая анимация графа")

    def draw_edge(self, v1, v2):
        self.canvas.create_line(v1[0], v1[1], v2[0], v2[1], fill="black", width=3)

    def draw_element(self, x, y, label, color):
        self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill=color)
        self.canvas.create_text(x, y, text=label, font=("Arial", 10))

    def update_logic(self, a, b, result):
        self.canvas.delete("logic")
        self.canvas.create_text(225, 225, text=f"A={a}", font=("Arial", 12), tags="logic")
        self.canvas.create_text(375, 225, text=f"B={b}", font=("Arial", 12), tags="logic")
        self.canvas.create_text(300, 300, text=f"Результат: {result}", font=("Arial", 14), tags="logic")

def main():
    root = tk.Tk()
    root.title("Главное окно")
    root.geometry("300x300")

    class Logger:
        def log(self, msg):
            print(msg)

    logger = Logger()
    anim = AnimationManager(logger)

    btn_graph = tk.Button(root, text="Анимация графа", command=anim.animate_graph)
    btn_graph.pack(pady=10)

    btn_set = tk.Button(root, text="Анимация множества", command=anim.animate_set)
    btn_set.pack(pady=10)

    btn_logic = tk.Button(root, text="Анимация логики", command=anim.animate_logic)
    btn_logic.pack(pady=10)

    btn_circle = tk.Button(root, text="Круговой граф (новая)", command=anim.animate_circle_graph)
    btn_circle.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
