from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox
import os

class image_editor_app:
    def __init__ (self, root):
        self.root = root
        self.root.title("Image Editor")
        self.root.geometry("1200x900")

        self.current_image = None
        self.original_image = None  # Store the original image
        self.photo = None
        self.scale_percent = 100  # Track the scale percentage
        self.transformations = []  # List to store transformation history

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

        # Create frame for main area
        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Create canvas for image display
        self.canvas = tk.Canvas(main_frame, width=700, height=500, bg="gray")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, padx=10)

        # Create edit frame
        edit_frame = tk.Frame(main_frame, bg = "lightblue", width=400)
        edit_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        # Add editor title
        edit_title = tk.Label(edit_frame, text="Edit Tools", font=("Arial", 16, "bold"), bg="lightblue", fg="black")
        edit_title.pack(padx=10)

        # create info box
        self.info_text = tk.Label(self.root, text="No image loaded.", font=("Arial", 10), fg="black", justify=tk.LEFT, bg="lightgray", padx=10, pady=10)
        self.info_text.pack(fill=tk.X, padx=20, pady=10)
        
        # Rotate Title
        rotate_title = tk.Label(edit_frame, text="Rotate Image", font=("Arial", 14, "bold"), bg="lightblue", fg="black")
        rotate_title.pack(padx=10, pady=5)

        # Create rotate frame
        rotate_frame = tk.Frame(edit_frame, bg="lightblue")
        rotate_frame.pack(padx=10, pady=5)

        # Create rotate buttons
        rotate_left_button = tk.Button(rotate_frame, text="Rotate Left", highlightbackground="lightblue", font=("Arial", 10), command=self.rotate_left)
        rotate_left_button.pack(padx=10, pady=5, side=tk.LEFT)

        rotate_right_button = tk.Button(rotate_frame, text="Rotate Right", highlightbackground="lightblue", font=("Arial", 10), command=self.rotate_right)
        rotate_right_button.pack(padx=10, pady=5, side=tk.LEFT)

        # Flip Title
        flip_title = tk.Label(edit_frame, text="Invert Image", font=("Arial", 14, "bold"), bg="lightblue", fg="black")
        flip_title.pack(padx=10, pady=5)

        # Create flip frame
        flip_frame = tk.Frame(edit_frame, bg="lightblue")
        flip_frame.pack(padx=10, pady=5)

        # Create flip buttons
        flip_vertical_button = tk.Button(flip_frame, text="Flip Vertical", highlightbackground="lightblue", font=("Arial", 10), command=self.flip_vertical)
        flip_vertical_button.pack(padx=10, pady=5, side=tk.LEFT)

        flip_horizontal_button = tk.Button(flip_frame, text="Flip Horizontal", highlightbackground="lightblue", font=("Arial", 10), command=self.flip_horizontal)
        flip_horizontal_button.pack(padx=10, pady=5, side=tk.LEFT)

        # Resize title
        resize_title = tk.Label(edit_frame, text="Resize Image", font=("Arial", 14, "bold"), bg="lightblue", fg="black")
        resize_title.pack(padx=10, pady=5)

        # Create resize slider
        self.resize_slider = tk.Scale(edit_frame, from_=10, to=200, orient=tk.HORIZONTAL, label="Resize (%)", bg="white", command=self.resize_image)
        self.resize_slider.set(100)
        self.resize_slider.pack(padx=10, pady=5)

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
                self.original_image = Image.open(file_path)  # Store the original
                self.current_image = self.original_image.copy()  # Work with a copy
                self.scale_percent = 100  # Reset scale to 100%
                self.resize_slider.set(100)  # Reset slider to 100%
                self.transformations = []  # Reset transformations
                self.display_image()
                self.display_info(file_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open image: {e}")

    def display_image(self):
        if self.current_image:
            # Get the canvas dimensions
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if canvas_width <= 1 or canvas_height <= 1:  # Canvas not properly initialized yet
                self.root.update_idletasks()  # Force geometry update
                canvas_width = self.canvas.winfo_width()
                canvas_height = self.canvas.winfo_height()
            
            # Create PhotoImage directly from current_image without any additional resizing
            self.photo = ImageTk.PhotoImage(self.current_image)
            self.canvas.delete("all")
            
            # Center the image in the canvas
            x = canvas_width / 2
            y = canvas_height / 2
            
            self.canvas.create_image(x, y, image=self.photo, anchor=tk.CENTER)

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

    def rotate_left(self):
        if self.current_image:
            self.transformations.append(('rotate', 90))
            self.apply_transformations()
            self.display_info("Rotated Left")

    def rotate_right(self):
        if self.current_image:
            self.transformations.append(('rotate', -90))
            self.apply_transformations()
            self.display_info("Rotated Right")

    def flip_vertical(self):
        if self.current_image:
            self.transformations.append(('flip_v', None))
            self.apply_transformations()
            self.display_info("Flipped Vertically")

    def flip_horizontal(self):
        if self.current_image:
            self.transformations.append(('flip_h', None))
            self.apply_transformations()
            self.display_info("Flipped Horizontally")

    def apply_transformations(self):
        if self.original_image:
            # Start with a fresh copy of the original image
            img = self.original_image.copy()
            print(self.transformations)
            
            # First apply the resize
            if self.scale_percent != 100:
                width = int(img.width * self.scale_percent / 100)
                height = int(img.height * self.scale_percent / 100)
                img = img.resize((width, height), Image.Resampling.LANCZOS)
            
            # Then apply all other transformations in order
            for transform_type, value in self.transformations:
                if transform_type == 'rotate':
                    img = img.rotate(value, expand=True)
                elif transform_type == 'flip_v':
                    img = img.transpose(Image.FLIP_TOP_BOTTOM)
                elif transform_type == 'flip_h':
                    img = img.transpose(Image.FLIP_LEFT_RIGHT)
            
            self.current_image = img
            self.display_image()

    def resize_image(self, value):
        if self.original_image:
            self.scale_percent = int(value)
            self.apply_transformations()
            self.display_info(f"Resized to {self.scale_percent}%")


if __name__ == "__main__":
    root = tk.Tk()
    app = image_editor_app(root)
    root.mainloop()