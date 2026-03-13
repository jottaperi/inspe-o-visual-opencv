import time
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox

img = None

def average_method(image):
    width, height = image.size
    new_image = Image.new("RGB", (width, height))

    pixels = image.load()
    new_pixels = new_image.load()

    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            gray = int((r + g + b) / 3)
            new_pixels[x, y] = (gray, gray, gray)

    return new_image


def luminosity_method(image):
    width, height = image.size
    new_image = Image.new("RGB", (width, height))

    pixels = image.load()
    new_pixels = new_image.load()

    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            new_pixels[x, y] = (gray, gray, gray)

    return new_image

def desaturation_method(image):
    width, height = image.size
    new_image = Image.new("RGB", (width, height))

    pixels = image.load()
    new_pixels = new_image.load()

    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            gray = int((max(r, g, b) + min(r, g, b)) / 2)
            new_pixels[x, y] = (gray, gray, gray)

    return new_image

def resize_image(image, max_size=350):
    width, height = image.size
    ratio = min(max_size / width, max_size / height)
    new_width = int(width * ratio)
    new_height = int(height * ratio)
    return image.resize((new_width, new_height))

def show_images(original, converted=None):

    original_resized = resize_image(original)
    tk_original = ImageTk.PhotoImage(original_resized)
    original_label.config(image=tk_original)
    original_label.image = tk_original

    if converted:
        converted_resized = resize_image(converted)
        tk_converted = ImageTk.PhotoImage(converted_resized)
        converted_label.config(image=tk_converted)
        converted_label.image = tk_converted

def load_image():
    global img

    file_path = filedialog.askopenfilename(
        filetypes=[("Imagens", "*.jpg *.png *.jpeg")]
    )

    if file_path:
        img = Image.open(file_path)
        show_images(img)

def convert_image():
    global img

    if img is None:
        messagebox.showerror("Erro", "Selecione uma imagem primeiro.")
        return

    method = method_var.get()

    start_time = time.time()

    if method == "average":
        new_img = average_method(img)
    elif method == "luminosity":
        new_img = luminosity_method(img)
    elif method == "desaturation":
        new_img = desaturation_method(img)
    else:
        return

    end_time = time.time()
    execution_time = end_time - start_time

    filename = f"imagem_{method}.jpg"
    new_img.save(filename)

    show_images(img, new_img)

    result_label.config(
        text=f"Método: {method} | Tempo: {execution_time:.4f} segundos\nImagem salva como {filename}"
    )

root = tk.Tk()
root.title("Conversor para Escala de Cinza")
root.geometry("900x650")
root.configure(bg="#f4f4f4")

method_var = tk.StringVar(value="average")

title_label = tk.Label(
    root,
    text="Conversor para Escala de Cinza",
    font=("Arial", 18, "bold"),
    bg="#f4f4f4",
    fg="#333"
)
title_label.pack(pady=15)

top_frame = tk.Frame(root, bg="#f4f4f4")
top_frame.pack(pady=10)

btn_load = tk.Button(
    top_frame,
    text="Selecionar Imagem",
    command=load_image,
    width=20,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 10, "bold")
)
btn_load.grid(row=0, column=0, padx=10)

btn_convert = tk.Button(
    top_frame,
    text="Converter",
    command=convert_image,
    width=20,
    bg="#2196F3",
    fg="white",
    font=("Arial", 10, "bold")
)
btn_convert.grid(row=0, column=1, padx=10)

methods_frame = tk.LabelFrame(
    root,
    text="Escolha o Método",
    font=("Arial", 12, "bold"),
    bg="#f4f4f4",
    padx=20,
    pady=10
)
methods_frame.pack(pady=10)

tk.Radiobutton(methods_frame, text="Average",
               variable=method_var, value="average",
               bg="#f4f4f4").pack(anchor="w")

tk.Radiobutton(methods_frame, text="Luminosity",
               variable=method_var, value="luminosity",
               bg="#f4f4f4").pack(anchor="w")

tk.Radiobutton(methods_frame, text="Desaturation",
               variable=method_var, value="desaturation",
               bg="#f4f4f4").pack(anchor="w")

image_frame = tk.Frame(root, bg="#f4f4f4")
image_frame.pack(pady=20)

original_label = tk.Label(
    image_frame,
    bg="white",
    bd=2,
    relief="solid"
)
original_label.grid(row=0, column=0, padx=20)

converted_label = tk.Label(
    image_frame,
    bg="white",
    bd=2,
    relief="solid"
)
converted_label.grid(row=0, column=1, padx=20)

result_label = tk.Label(
    root,
    text="",
    font=("Arial", 10),
    bg="#f4f4f4",
    fg="#444"
)
result_label.pack(pady=10)

root.mainloop()

