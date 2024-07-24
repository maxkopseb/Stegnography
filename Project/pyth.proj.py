import cv2
import string
import os
import uuid
from tkinter import Tk, Label, Button, Entry, Text, filedialog, messagebox

# Initialize dictionaries for character-to-ASCII and ASCII-to-character mapping
d = {}
c = {}
for i in range(255):
    d[chr(i)] = i
    c[i] = chr(i)

# Function to hide text in image
def hide_text_in_image(image_path, key, text):
    text += "\0"  # Append a null character as the delimiter
    x = cv2.imread(image_path)
    if x is None:
        messagebox.showerror("Error", "Could not open or find the image.")
        return
    
    i = x.shape[0]
    j = x.shape[1]
    
    kl = 0
    z = 0
    n = 0
    m = 0
    l = len(text)

    for i in range(l):
        x[n, m, z] = d[text[i]] ^ d[key[kl]]
        n += 1
        m = (m + 1) % 3
        kl = (kl + 1) % len(key)

    # Save the encrypted image with a unique filename
    encrypted_image_path = f"encrypted_img_{uuid.uuid4().hex}.png"
    cv2.imwrite(encrypted_image_path, x)
    messagebox.showinfo("Success", f"Data hiding done. Encrypted image saved as {encrypted_image_path}")

# Function to extract text from the encrypted image
def extract_text_from_image(key, image_path):
    x = cv2.imread(image_path)
    if x is None:
        messagebox.showerror("Error", "Could not open or find the image.")
        return

    kl = 0
    z = 0
    n = 0
    m = 0
    decrypt = ""

    try:
        while True:
            char = c[x[n, m, z] ^ d[key[kl]]]
            if char == "\0":  # Stop if the delimiter is found
                break
            decrypt += char
            n += 1
            m = (m + 1) % 3
            kl = (kl + 1) % len(key)
    except KeyError:
        return None
    
    return decrypt

# GUI setup
def select_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        image_path_entry.delete(0, 'end')
        image_path_entry.insert(0, file_path)

def encrypt_image():
    image_path = image_path_entry.get()
    key = key_entry.get()
    text = text_entry.get("1.0", 'end-1c')
    if not image_path or not key or not text:
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    hide_text_in_image(image_path, key, text)

def decrypt_image():
    image_path = image_path_entry.get()
    key = key_entry.get()
    if not image_path or not key:
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    try:
        decrypted_text = extract_text_from_image(key, image_path)
    except IndexError:
        messagebox.showerror("Error", "Wrong Key, Please try again")
    else:
        if decrypted_text is None:
            messagebox.showerror("Error", "Wrong Key, Please try again")
        else:
            text_entry.delete("1.0", 'end')
            text_entry.insert("1.0", decrypted_text)
# Main application window
root = Tk()
root.title("Image Steganography")

Label(root, text="Image Path:").grid(row=0, column=0, padx=10, pady=10)
image_path_entry = Entry(root, width=50)
image_path_entry.grid(row=0, column=1, padx=10, pady=10)
Button(root, text="Browse", command=select_image).grid(row=0, column=2, padx=10, pady=10)

Label(root, text="Key:").grid(row=1, column=0, padx=10, pady=10)
key_entry = Entry(root, width=50)
key_entry.grid(row=1, column=1, padx=10, pady=10)

Label(root, text="Text:").grid(row=2, column=0, padx=10, pady=10)
text_entry = Text(root, width=50, height=10)
text_entry.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

Button(root, text="Encrypt Image", command=encrypt_image).grid(row=3, column=1, padx=10, pady=10)
Button(root, text="Decrypt Image", command=decrypt_image).grid(row=3, column=2, padx=10, pady=10)

root.mainloop()
