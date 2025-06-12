import tkinter as tk
from PIL import Image, ImageTk
import random
import string
import re

def load_banned_passwords(filename):
    with open(filename, "r", encoding="utf-8", errors="ignore") as file:
        return set(line.strip().lower() for line in file)

banned_passwords = load_banned_passwords("PwnedPasswordsTop100k.txt")

def check_password_strength(password, banned_passwords):
    feedback = []

    if password.lower() in banned_passwords:
        feedback.append("❌ Your password is in Top 100K pwned passwords!")

    if len(password) < 8:
        feedback.append("❌ Password is too short (8 characters minimum!)")

    if not re.search(r"[A-Z]", password):
        feedback.append("❌ No uppercase character detected!")

    if not re.search(r"[a-z]", password):
        feedback.append("❌ No lowercase character detected!")

    if not re.search(r"\d", password):
        feedback.append("❌ No number detected!")

    if not re.search(r"[^A-Za-z0-9]", password):
        feedback.append("❌ No special character detected!")

    if not feedback:
        return ["✅ Your password is strong!"]
    return feedback

def on_check():
    password = entry.get()
    result = check_password_strength(password, banned_passwords)
    result_label.config(text="\n".join(result), fg="green" if "✅" in result[0] else "red")

def toggle_password():
    entry.config(show="" if show_var.get() else "*")

def generate_password(length=12):
    if length < 8:
        length = 8
    upper = random.choice(string.ascii_uppercase)
    lower = random.choice(string.ascii_lowercase)
    digit = random.choice(string.digits)
    special = random.choice(string.punctuation)
    remaining = length - 4
    others = random.choices(string.ascii_letters + string.digits + string.punctuation, k=remaining)
    password_characters = list(upper + lower + digit + special + ''.join(others))
    random.shuffle(password_characters)
    password = ''.join(password_characters)
    entry.delete(0, tk.END)
    entry.insert(0, password)
    result_label.config(text="✅ Strong Password generated!", fg="green")

def clear_field():
    entry.delete(0, tk.END)
    result_label.config(text="")

root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("800x600")
root.resizable(False, False)

bg_image = Image.open("background.png")
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

frame = tk.Frame(root, bg="#1d2b3a")
frame.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(frame, text="Enter Your Password:", font=("Arial", 12, "bold"), bg="#1d2b3a", fg="white").pack(pady=(10, 5))

entry = tk.Entry(frame, show="*", width=30, font=("Arial", 12), bg="#2a3f54", fg="white", insertbackground="white")
entry.pack(pady=5)

show_var = tk.BooleanVar()
tk.Checkbutton(frame, text="Show Password", variable=show_var, command=toggle_password,
               bg="#1d2b3a", fg="white", selectcolor="#1d2b3a", activebackground="#1d2b3a").pack(pady=5)

tk.Button(frame, text="Check Password", command=on_check, font=("Arial", 12),
          bg="#1c2e40", fg="white", activebackground="#2a3f54").pack(pady=10)

result_label = tk.Label(frame, text="", font=("Arial", 10), bg="#1d2b3a", fg="white", wraplength=350, justify="left")
result_label.pack(pady=5)

tk.Button(frame, text="Generate Strong Password", command=generate_password,
          bg="#1d2b3a", fg="white", font=("Arial", 12)).pack(pady=5)

tk.Button(frame, text="Clear", command=clear_field,
          bg="#1d2b3a", fg="white", font=("Arial", 12)).pack(pady=5)

root.bind("<Return>", lambda event: on_check())

root.mainloop()
