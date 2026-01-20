import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pyttsx3

engine = pyttsx3.init()
stego_image_path = "stego_image.png"
img = None
tk_img = None

def preprocess_image(path):
    image = Image.open(path).convert("L")
    image = image.resize((128, 128))
    return image

def select_image():
    global img, tk_img
    path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
    )

    if not path:
        return

    img = preprocess_image(path)

    # Display grayscale image
    display_img = img.resize((200, 200))
    tk_img = ImageTk.PhotoImage(display_img)
    image_label.config(image=tk_img)

    messagebox.showinfo("Image Selected", "Grayscale image (128×128) displayed")

def hide_character():
    global img
    if img is None:
        messagebox.showerror("Error", "Select an image first")
        return

    char = entry_char.get()
    if len(char) != 1:
        messagebox.showerror("Error", "Enter one character only")
        return

    binary = format(ord(char), '08b')
    pixels = img.load()
    idx = 0

    for i in range(128):
        for j in range(128):
            if idx < 8:
                pixels[j, i] = (pixels[j, i] & ~1) | int(binary[idx])
                idx += 1

    img.save(stego_image_path)
    messagebox.showinfo("Success", "Character hidden successfully")

def retrieve_character():
    try:
        img2 = Image.open(stego_image_path)
    except:
        messagebox.showerror("Error", "Stego image not found")
        return

    pixels = img2.load()
    binary = ""

    for i in range(128):
        for j in range(128):
            if len(binary) < 8:
                binary += str(pixels[j, i] & 1)

    char = chr(int(binary, 2))
    result_label.config(text=f"Hidden Character: {char}")

    engine.say(char)
    engine.runAndWait()

# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("Steganography with Grayscale Preview")
root.geometry("450x520")

tk.Label(root, text="Steganography Assignment", font=("Arial", 14, "bold")).pack(pady=10)

tk.Button(root, text="Select Image", command=select_image, width=25).pack(pady=5)

image_label = tk.Label(root)
image_label.pack(pady=10)

tk.Label(root, text="Enter Character to Hide").pack()
entry_char = tk.Entry(root, width=10)
entry_char.pack(pady=5)

tk.Button(root, text="Hide Character", command=hide_character, width=25).pack(pady=5)
tk.Button(root, text="Retrieve Character", command=retrieve_character, width=25).pack(pady=5)

result_label = tk.Label(root, text="Hidden Character: ", font=("Arial", 12))
result_label.pack(pady=10)

root.mainloop()
