from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox

class image_editor_app:
    def __init__ (self, root):
        self.root = root
        self.root.title("Image Editor")
        self.root.geometry("800x600")

if __name__ == "__main__":
    root = tk.Tk()
    app = image_editor_app(root)
    root.mainloop()