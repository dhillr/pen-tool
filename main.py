import tkinter as tk
from tkinter import messagebox, colorchooser

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.startX = 0
        self.startY = 0
        self.dragged = False


        self.title("pen tool :D")
        self.geometry("600x800")

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Motion>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)

        self.pen_label = tk.Label(self, text="pen size")
        self.pen_label.pack()
        self.size_slider = tk.Scale(self, from_=1, to=20, orient=tk.HORIZONTAL, command=self.set_pen_size)
        self.size_slider.pack()
        self.size_slider.set(3)

        self.color_button = tk.Button(self, text="pick color", command=self.pick)
        self.color_button.pack()
        tk.Button(self, text="toggle eraser", command=self.eraser_mode).pack()

        self.strokes = []
        self.pen_size = 3
        self.eraser_size = 10
        self.color = "black"

        self.eraser = False

        self.mouseX = 0
        self.mouseY = 0

        self.init()

    def init(self):
        self.canvas.delete("all")

        for stroke in self.strokes:
            self.canvas.create_line(stroke[0], stroke[1], stroke[2], stroke[3], fill=stroke[5], width=stroke[4], joinstyle="round", capstyle="round")

        # size: float = self.pen_size if not self.eraser else self.eraser_size
        # self.canvas.create_oval(float(self.mouseX) - 0.5 * float(size), float(self.mouseY) - 0.5 * float(size), float(self.mouseX) + 0.5 * float(size), float(self.mouseY) + 0.5 * float(size))

        self.after(1, self.init)
        self.dragged = False
    
    def set_pen_size(self, v):
        if self.eraser:
            self.eraser_size = v
        else:
            self.pen_size = v

    def on_mouse_press(self, event: tk.Event):
        self.mouseX = event.x
        self.mouseY = event.y
        
        if not self.dragged: 
            self.startX = event.x
            self.startY = event.y

    def on_mouse_drag(self, event: tk.Event):
        self.dragged = True

        self.strokes.append([self.startX, self.startY, event.x, event.y, self.pen_size if not self.eraser else self.eraser_size, self.color if not self.eraser else "white"])

        if self.startX != event.x:
            self.startX = event.x
        if self.startY != event.y:
            self.startY = event.y

    def pick(self):
        self.color = colorchooser.askcolor()[1]

    def eraser_mode(self):
        
        self.eraser = not self.eraser
        self.pen_label.config(text="eraser size" if self.eraser else "pen size")
        if self.eraser:
            self.size_slider.config(from_=1, to=100, resolution=1)
            self.size_slider.set(self.eraser_size)
        else:
            self.size_slider.config(from_=1, to=20, resolution=1)
            self.size_slider.set(self.pen_size)

App().mainloop()