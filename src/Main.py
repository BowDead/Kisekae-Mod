import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cairosvg
import io

class KisekaeRemake(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Kisekae Remake")
        self.geometry("900x600")

        self.columnconfigure(0, weight=1, minsize=150)
        self.columnconfigure(1, weight=4)
        self.columnconfigure(2, weight=1, minsize=150)
        self.rowconfigure(0, weight=1)

        # Tworzenie zakładek w panelach
        self.create_left_panel()
        self.create_canvas()
        self.create_right_panel()

        # Bind do przeciągania
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        self._drag_data = {"x": 0, "y": 0}

        # Załaduj obraz z SVG
        self.svg_image_orig = self.load_svg_image("../resources/testball.svg")

        self.image_id = None
        # Relatywna pozycja obrazu (środek canvasu)
        self.image_rel_pos = (0.5, 0.5)
        self.image_pixel_pos = (0, 0)

        self.image_on_canvas = False  # Flaga stanu obrazu

    def create_left_panel(self):
        self.left_panel = ttk.Notebook(self)
        self.left_panel.grid(row=0, column=0, sticky="nswe")

        tab1 = ttk.Frame(self.left_panel)
        tab2 = ttk.Frame(self.left_panel)

        self.left_panel.add(tab1, text="Zakładka 1")
        self.left_panel.add(tab2, text="Zakładka 2")

        ttk.Label(tab1, text="Lewy panel - Zakładka 1").pack(padx=10, pady=10)
        ttk.Label(tab2, text="Lewy panel - Zakładka 2").pack(padx=10, pady=10)

    def create_canvas(self):
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.grid(row=0, column=1, sticky="nswe")

    def create_right_panel(self):
        self.right_panel = ttk.Notebook(self)
        self.right_panel.grid(row=0, column=2, sticky="nswe")

        tab1 = ttk.Frame(self.right_panel)
        tab2 = ttk.Frame(self.right_panel)

        self.right_panel.add(tab1, text="Zakładka 1")
        self.right_panel.add(tab2, text="Zakładka 2")

        ttk.Label(tab1, text="Prawy panel - Zakładka 1").pack(padx=10, pady=10)

        # Przyciski do dodawania/usuwania obiektów na kanwie
        self.toggle_button = ttk.Button(tab1, text="Dodaj Obiekt", command=self.toggle_image)
        self.toggle_button.pack(pady=10)

    def load_svg_image(self, filename, size=(100, 100)):
        png_data = cairosvg.svg2png(url=filename)
        image = Image.open(io.BytesIO(png_data))
        image = image.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)

    def draw_image(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 10 or h < 10:
            # Canvas jeszcze nie gotowy
            self.after(100, self.draw_image)
            return

        x = int(self.image_rel_pos[0] * w)
        y = int(self.image_rel_pos[1] * h)
        self.image_pixel_pos = (x, y)

        if self.image_id is None:
            self.image_id = self.canvas.create_image(x, y, image=self.svg_image_orig)
        else:
            self.canvas.coords(self.image_id, x, y)

    def toggle_image(self):
        if self.image_on_canvas:
            # Usuń obraz
            self.canvas.delete(self.image_id)
            self.image_id = None
            self.image_on_canvas = False
            self.toggle_button.config(text="Dodaj Obiekt")
        else:
            # Dodaj obraz
            self.draw_image()
            self.image_on_canvas = True
            self.toggle_button.config(text="Usuń Obiekt")

    def on_canvas_resize(self, event):
        if self.image_on_canvas:
            self.draw_image()

    def on_button_press(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def on_move_press(self, event):
        dx = event.x - self._drag_data["x"]
        dy = event.y - self._drag_data["y"]

        # Przesuwamy obraz o dx, dy - ale musimy też aktualizować relatywną pozycję!
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        new_x = self.image_pixel_pos[0] + dx
        new_y = self.image_pixel_pos[1] + dy

        # Zapewnij, że nie wyjdzie poza canvas (opcjonalnie)
        new_x = max(0, min(new_x, w))
        new_y = max(0, min(new_y, h))

        # Aktualizuj relatywne współrzędne
        self.image_rel_pos = (new_x / w, new_y / h)
        self.image_pixel_pos = (new_x, new_y)

        self.canvas.coords(self.image_id, new_x, new_y)

        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

if __name__ == "__main__":
    app = KisekaeRemake()
    app.mainloop()
