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
    else:
        feedback.append("✅ Your password is not in Top 100K pwned passwords.")

    if len(password) < 8:
        feedback.append("❌ Password is too short (8 characters minimum!)")
    else:
        feedback.append("✅ Your password has good length!")

    if not re.search(r"[A-Z]", password):
        feedback.append("❌ No uppercase character detected!")
    else:
        feedback.append("✅ Uppercase character detected!")

    if not re.search(r"[a-z]", password):
        feedback.append("❌ No lowercase character detected!")
    else:
        feedback.append("✅ Lowercase character detected!")

    if not re.search(r"\d", password):
        feedback.append("❌ No number detected!")
    else:
        feedback.append("✅ Number detected!")

    if not re.search(r"[^A-Za-z0-9]", password):
        feedback.append("❌ No special character detected!")
    else:
        feedback.append("✅ Special character detected!")
    return feedback

def get_strength_score(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"\d", password):
        score += 1
    if re.search(r"[^A-Za-z0-9]", password):
        score += 1
    return score

def on_check():
    password = entry.get()
    result = check_password_strength(password, banned_passwords)

    for widget in result_frame.winfo_children():
        widget.destroy()

    for line in result:
        color = "green" if line.startswith("✅") else "red"
        label = tk.Label(result_frame, text=line, font=("Arial", 10), bg="#1d2b3a", fg=color, anchor="w", justify="left")
        label.pack(anchor="w")

    strength = get_strength_score(password)
    strength_canvas.delete("all")
    segment_width = 40
    colors = ["red", "orange", "yellow", "yellowgreen", "green"]
    for i in range(5):
        fill_color = colors[i] if i < strength else "#ccc"
        strength_canvas.create_rectangle(i * segment_width, 0, (i + 1) * segment_width, 20, fill=fill_color, outline="")

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
    on_check()

def clear_field():
    entry.delete(0, tk.END)
    result_label.config(text="")
    for widget in result_frame.winfo_children():
        widget.destroy()
    strength_canvas.delete("all")

def toggle_fullscreen():
    root.attributes("-fullscreen", True)

def exit_fullscreen():
    root.attributes("-fullscreen", False)

root = tk.Tk()
root.title("Password Strength Checker")
root.attributes("-fullscreen", False)
root.geometry("800x600")
root.bind("<F11>", lambda e: toggle_fullscreen())
root.bind("<Escape>", lambda e: exit_fullscreen())

bg_image = Image.open("background.png")
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

def resize_bg(event):
    global bg_photo
    new_image = bg_image.resize((event.width, event.height), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(new_image)
    bg_label.config(image=bg_photo)
    bg_label.image = bg_photo

root.bind("<Configure>", resize_bg)

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

strength_canvas = tk.Canvas(frame, width=200, height=20, bg="#ccc", highlightthickness=0)
strength_canvas.pack(pady=5)

result_frame = tk.Frame(frame, bg="#1d2b3a")
result_frame.pack(pady=5)

tk.Button(frame, text="Generate Strong Password", command=generate_password,
          bg="#1d2b3a", fg="white", font=("Arial", 12)).pack(pady=5)

tk.Button(frame, text="Clear", command=clear_field,
          bg="#1d2b3a", fg="white", font=("Arial", 12)).pack(pady=5)

root.bind("<Return>", lambda event: on_check())
root.mainloop()