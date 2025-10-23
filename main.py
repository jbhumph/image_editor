from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox
import os

class image_editor_app:
    def __init__ (self, root):
        self.root = root
        self.root.title("Image Editor")
        self.root.geometry("600x900")

        self.current_image = None
        self.photo = None

        self.create_widgets()

    def create_widgets(self):
        # Create top frame
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        # Create title label
        title_label = tk.Label(top_frame, text="Simple Image Editor", font=("Arial", 32, "bold"), fg="#92b0e0")
        title_label.pack(side=tk.LEFT, padx=10)

        # Create open button
        open_button = tk.Button(top_frame, text="Open Image", command=self.open_image)
        open_button.pack(side=tk.LEFT, padx=10)

        # Create canvas for image display
        self.canvas = tk.Canvas(self.root, width=700, height=500, bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True, pady=10)

        # create info box
        self.info_text = tk.Label(self.root, text="No image loaded.", font=("Arial", 10), fg="black", justify=tk.LEFT, bg="lightgray", padx=10, pady=10)
        self.info_text.pack(fill=tk.X, padx=20, pady=10)
        
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
                self.display_info(file_path)
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

    def display_info(self, file_path):
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path) / 1024  # size in KB

        img_format = self.current_image.format
        img_dimensions = self.current_image.size

        info = f"File Name: {file_name}\nSize: {file_size:.2f} KB\nFormat: {img_format}\nDimensions: {img_dimensions[0]} x {img_dimensions[1]} pixels"

        self.info_text.config(text=info)

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