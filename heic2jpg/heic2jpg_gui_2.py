from PIL import Image, ImageTk
import pillow_heif
import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar
from tkinter import messagebox

def convert_heic_to_jpg(heic_path, jpg_path):
    heic_image = pillow_heif.read_heif(heic_path)
    image = Image.frombytes(
        heic_image.mode,
        heic_image.size,
        heic_image.data,
        "raw",
        heic_image.mode,
        heic_image.stride,
    )
    image.save(jpg_path, "JPEG")

def browse_files():
    filetypes = (("HEIC Files", "*.heic"), ("All Files", "*.*"))
    filenames = filedialog.askopenfilenames(filetypes=filetypes)
    for file in filenames:
        photo_files.append(file)
    update_preview_canvas()

def update_preview_canvas():
    global photo_references
    canvas.delete("all")  # Clear previous images on the canvas
    y_position = 10  # Starting y-position for images
    x_position = 10  # Starting x-position for images

    photo_references = []

    for file in photo_files:
        heic_image = pillow_heif.read_heif(file)
        pil_image = Image.frombytes(
            heic_image.mode,
            heic_image.size,
            heic_image.data,
            "raw",
            heic_image.mode,
            heic_image.stride,
        )
        pil_image.thumbnail((200, 200))  # Resize preview image
        photo = ImageTk.PhotoImage(pil_image)
        photo_references.append(photo)  # Keep a reference to the PhotoImage
        canvas.create_image(x_position, y_position, anchor="nw", image=photo)
        x_position += 210  # Increment x-position for the next image

        # If x_position exceeds 420 (2 images per row), reset it to 10 and move to the next row
        if x_position > 420:
            x_position = 10
            y_position += 210

    # Update the canvas scroll region to fit all images
    canvas.configure(scrollregion=canvas.bbox("all"))

def convert_images():
    save_directory = filedialog.askdirectory()
    num_files = len(photo_files)
    progress_bar["maximum"] = num_files
    for index, file in enumerate(photo_files, 1):
        jpg_file = save_directory + "/" + file.split("/")[-1].split(".")[0] + ".jpg"
        convert_heic_to_jpg(file, jpg_file)
        progress_bar["value"] = index
        window.update()
    messagebox.showinfo("Conversion Complete", "All files have been converted!")

# Create main window
window = tk.Tk()
window.title("HEIC to JPG Converter")

# Create buttons and image frame
browse_button = tk.Button(window, text="Browse Files", command=browse_files)
browse_button.pack()

# Create canvas for image preview with scrollbar
canvas_frame = tk.Frame(window)
canvas_frame.pack(fill="both", expand=True)

canvas = tk.Canvas(canvas_frame)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(canvas_frame, command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar.set)

# Bind canvas resizing to update the scroll region
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

convert_button = tk.Button(window, text="Convert", command=convert_images)
convert_button.pack()

photo_files = []

# Create progress bar
progress_bar = Progressbar(window, orient=tk.HORIZONTAL, length=300, mode="determinate")
progress_bar.pack()

# Run the main event loop
window.mainloop()