import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cairosvg
import io
from dataclasses import dataclass

@dataclass
class BodyPart:
    imgsource: str              # Ścieżka do pliku obrazu (np. SVG)
    offset: tuple               # (x_offset, y_offset) względem centrum ciała
    initial_position: tuple = (0, 0)  # (x_init, y_init) dla początkowej pozycji
    part_type: str = ""         # Typ elementu (np. "head", "arm", "leg")

class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parts = []

    def add_part(self, part: BodyPart):
        self.parts.append(part)

class KisekaeRemake(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Kisekae Remake")
        self.geometry("900x600")

        self.columnconfigure(0, weight=1, minsize=150)
        self.columnconfigure(1, weight=4)
        self.columnconfigure(2, weight=1, minsize=150)
        self.rowconfigure(0, weight=1)

        self.left_panel = ttk.Frame(self, relief=tk.SUNKEN)
        self.left_panel.grid(row=0, column=0, sticky="nswe")

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.grid(row=0, column=1, sticky="nswe")

        self.right_panel = ttk.Frame(self, relief=tk.SUNKEN)
        self.right_panel.grid(row=0, column=2, sticky="nswe")

        ttk.Label(self.left_panel, text="Lewy panel UI").pack(padx=10, pady=10)
        ttk.Label(self.right_panel, text="Prawy panel UI").pack(padx=10, pady=10)

        self.character = Character(450, 300)  # Pozycja środka canvasu
        head = BodyPart(
            imgsource="../resources/testball.svg",
            offset=(0, 0),
            initial_position=(0, -50),  # Głowa jest trochę wyżej niż centrum ciała
            part_type="head"
        )
        self.character.add_part(head)

        self.images = {}  # cache obrazów PhotoImage, by nie były usuwane przez GC
        self.draw_character()

    def load_svg_image(self, filepath, size=(200, 200)):
        png_data = cairosvg.svg2png(url=filepath)
        image = Image.open(io.BytesIO(png_data))
        image = image.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)

    def draw_character(self):
        self.canvas.delete("all")
        for i, part in enumerate(self.character.parts):
            img = self.load_svg_image(part.imgsource)
            self.images[i] = img
            x = self.character.x + part.offset[0] + part.initial_position[0]
            y = self.character.y + part.offset[1] + part.initial_position[1]
            self.canvas.create_image(x, y, image=img)

if __name__ == "__main__":
    app = KisekaeRemake()
    app.mainloop()
