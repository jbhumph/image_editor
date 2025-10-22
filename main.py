from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox

class image_editor_app:
    def __init__ (self, root):
        self.root = root
        self.root.title("Image Editor")
        self.root.geometry("800x600")

        self.current_image = None
        self.photo = None

        self.create_widgets()

    def create_widgets(self):
        open_button = tk.Button(self.root, text="Open Image", command=self.open_image)
        open_button.pack(pady=10)

        self.canvas = tk.Canvas(self.root, width=700, height=500, bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Bind window resize event
        self.root.bind('<Configure>', self.on_window_resize)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[
            ("Image Files", ("*.png", "*.jpg", "*.jpeg", "*.bmp", "*.gif")),
            ("PNG Files", "*.png"),
            ("JPEG Files", ("*.jpg", "*.jpeg")),
            ("BMP Files", "*.bmp"),
            ("GIF Files", "*.gif")
        ])
        if file_path:
            try:
                self.current_image = Image.open(file_path)
                self.display_image(self.current_image)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open image: {e}")

    def display_image(self, image=None):
        if self.current_image:
            # Get the canvas dimensions
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if canvas_width <= 1 or canvas_height <= 1:  # Canvas not properly initialized yet
                self.root.update_idletasks()  # Force geometry update
                canvas_width = self.canvas.winfo_width()
                canvas_height = self.canvas.winfo_height()
            
            # Get the image dimensions
            img_width, img_height = self.current_image.size
            
            # Calculate the scaling factor to fit the image within the canvas
            width_ratio = canvas_width / img_width
            height_ratio = canvas_height / img_height
            scale_factor = min(width_ratio, height_ratio)
            
            # Calculate new dimensions
            new_width = int(img_width * scale_factor)
            new_height = int(img_height * scale_factor)
            
            # Resize the image while maintaining aspect ratio
            resized_image = self.current_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            self.photo = ImageTk.PhotoImage(resized_image)
            self.canvas.delete("all")
            self.canvas.create_image(canvas_width/2, canvas_height/2, image=self.photo, anchor=tk.CENTER)
            
    def on_window_resize(self, event):
        # Only redraw if we have an image and if the resize event is for the main window
        if self.current_image and event.widget == self.root:
            # Add a small delay to prevent rapid redraws during resize
            self.root.after_cancel(self._after_id) if hasattr(self, '_after_id') else None
            self._after_id = self.root.after(100, self.display_image)




if __name__ == "__main__":
    root = tk.Tk()
    app = image_editor_app(root)
    root.mainloop()