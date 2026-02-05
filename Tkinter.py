from Image_processing import ImageProcessor
from Image_History import ImageHistory

import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk

class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing Application")
        self.root.geometry("1000x600")

        self.processor = ImageProcessor()
        self.history = ImageHistory()
        self.create_menu()
        self.create_widgets()
        self.create_status_bar()

    # ---------------- GUI SETUP ---------------- #
    def create_menu(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_image)
        file_menu.add_command(label="Save", command=self.save_image)
        file_menu.add_command(label="Save As", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)

        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        self.root.config(menu=menubar)

    def create_widgets(self):
        self.canvas = tk.Label(self.root)
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
 
        panel = tk.Frame(self.root)
        panel.pack(side=tk.RIGHT, fill=tk.Y)
 
        tk.Button(panel, text="Grayscale", command=self.apply_grayscale).pack(fill=tk.X)
        tk.Button(panel, text="Edge Detection", command=self.apply_edges).pack(fill=tk.X)
 
        # -------- Sliders (Non-Destructive) -------- #
        tk.Label(panel, text="Blur").pack()
        self.blur_slider = tk.Scale(panel, from_=0, to=10, orient=tk.HORIZONTAL, command=self.preview_adjustments)
        self.blur_slider.pack(fill=tk.X)
 
        tk.Label(panel, text="Brightness").pack()
        self.brightness_slider = tk.Scale(panel, from_=-100, to=100, orient=tk.HORIZONTAL, command=self.preview_adjustments)
        self.brightness_slider.pack(fill=tk.X)
 
        tk.Label(panel, text="Contrast").pack()
        self.contrast_slider = tk.Scale(panel, from_=1, to=3, resolution=0.1, orient=tk.HORIZONTAL, command=self.preview_adjustments)
        self.contrast_slider.set(1)
        self.contrast_slider.pack(fill=tk.X)
 
        tk.Button(panel, text="Apply Adjustments", command=self.commit_adjustments).pack(fill=tk.X, pady=5)
 
        # -------- Transform Buttons -------- #
        tk.Button(panel, text="Rotate 90°", command=lambda: self.rotate(90)).pack(fill=tk.X)
        tk.Button(panel, text="Rotate 180°", command=lambda: self.rotate(180)).pack(fill=tk.X)
        tk.Button(panel, text="Rotate 270°", command=lambda: self.rotate(270)).pack(fill=tk.X)
 
        tk.Button(panel, text="Flip Horizontal", command=lambda: self.flip("horizontal")).pack(fill=tk.X)
        tk.Button(panel, text="Flip Vertical", command=lambda: self.flip("vertical")).pack(fill=tk.X)
 
        tk.Button(panel, text="Resize 50%", command=lambda: self.resize(0.5)).pack(fill=tk.X)
        tk.Button(panel, text="Resize 150%", command=lambda: self.resize(1.5)).pack(fill=tk.X)
 
    def create_status_bar(self):
        self.status = tk.Label(self.root, text="No image loaded", relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
 
    # ---------------- CORE LOGIC ---------------- #
    def update_display(self):
        image = cv2.cvtColor(self.processor.image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image.thumbnail((600, 500))
        self.tk_image = ImageTk.PhotoImage(image)
        self.canvas.config(image=self.tk_image)
 
        h, w = self.processor.image.shape[:2]
        self.status.config(text=f"{self.processor.filename} | {w} x {h}")
 
    def reset_sliders(self):
        self.blur_slider.set(0)
        self.brightness_slider.set(0)
        self.contrast_slider.set(1)

    # ---------------- FILE OPERATIONS ---------------- #
    def open_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.bmp")])
        if path:
            self.processor.load_image(path)
            self.history.save(self.processor.image)
            self.update_display()
            self.reset_sliders()
    
    def save_image(self):
        if self.processor.image is not None:
            cv2.imwrite(self.processor.filepath, self.processor.image)
            messagebox.showinfo("Save Image", "Image saved successfully!")
        else:
            messagebox.showwarning("Save Image", "No image to save.")
    
    def save_as(self):
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("BMP files", "*.bmp")])
        if path:
            cv2.imwrite(path, self.processor.image)
            messagebox.showinfo("Save Image", "Image saved successfully!")
    
    # ---------------- EDIT OPERATIONS ---------------- #
    def undo(self):
        self.processor.image = self.history.undo(self.processor.image)
        self.processor.original_image = self.processor.image.copy()
        self.update_display()
        self.reset_sliders()
    
    def redo(self):
        self.processor.image = self.history.redo(self.processor.image)
        self.processor.original_image = self.processor.image.copy()
        self.update_display()
        self.reset_sliders()

    # -------------- IMAGE TRANSFORMATIONS ---------------- #
    def apply_grayscale(self):
        self.history.save(self.processor.image) 
        self.processor.to_grayscale()
        self.processor.original_image = self.processor.image.copy()
        self.update_display()
    
    def apply_edges(self):
        self.history.save(self.processor.image)
        self.processor.edge_detection()
        self.processor.original_image = self.processor.image.copy()
        self.update_display()

    def rotate(self, angle):
        self.history.save(self.processor.image)
        self.processor.rotate(angle)
        self.processor.original_image = self.processor.image.copy()
        self.update_display()

    def flip(self, mode):
        self.history.save(self.processor.image)
        self.processor.flip(mode)
        self.processor.original_image = self.processor.image.copy()
        self.update_display()

    def resize(self, scale):
        self.history.save(self.processor.image)
        self.processor.resize(scale)
        self.processor.original_image = self.processor.image.copy()
        self.update_display()

    # -------------- Slider Operations ---------------- #
    def preview_adjustments(self, _):
        self.processor.reset_to_original()
        self.processor.blur(self.blur_slider.get())
        self.processor.adjust_brightness(self.brightness_slider.get())
        self.processor.adjust_contrast(self.contrast_slider.get())
        self.update_display()
    
    def commit_adjustments(self):
        self.history.save(self.processor.image)
        self.processor.original_image = self.processor.image.copy()
        self.update_display()
        messagebox.showinfo("Adjustments Applied", "Adjustments have been applied to the image.")

# ======================================================
# Program Entry Point
# ======================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()
