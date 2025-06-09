
import tkinter as tk
from PIL import Image, ImageTk
from password_checker import check_password_strength, load_banned_passwords
import random
import string 

banned_passwords = load_banned_passwords("PwnedPasswordsTop100k.txt")

def on_check():
    password = entry.get()
    result = check_password_strength(password, banned_passwords)
    result_label.config(text="\n".join(result), fg="green" if "✅" in result[0] else "red")

def toggle_password():
    entry.config(show="" if show_var.get() else "*")

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
show_check = tk.Checkbutton(frame, text="Show Password", variable=show_var, command=toggle_password,
                            bg="#1d2b3a", fg="white", selectcolor="#1d2b3a", activebackground="#1d2b3a")
show_check.pack(pady=5)

tk.Button(frame, text="Check Password", command=on_check, font=("Arial", 12),
          bg="#1c2e40", fg="white", activebackground="#2a3f54").pack(pady=10)

result_label = tk.Label(frame, text="", font=("Arial", 10), bg="#1d2b3a", fg="white", wraplength=350, justify="left")
result_label.pack(pady=5)

root.bind("<Return>" , lambda event: on_check())

def generate_password(length = 12):
    if length < 8:
        length = 8
    
    upper = random.choice(string.ascii_uppercase)
    lower = random.choice(string.ascii_lowercase)
    digit = random.choice(string.digits)
    special = random.choice(string.punctuation)
    
    remaining = length - 4
    others = random.choices(string.ascii_letters + string.digits + string.punctuation, k= remaining)
    password_characters = list(upper + lower + digit + special + ''.join(others))
    random.shuffle(password_characters)
    password = ''.join(password_characters)
    
    entry.delete(0, tk.END)
    entry.insert(0 , password)
    result_label.config(text = "✅ Strong Password generated!" , fg="green")


tk.Button(root, text = "Generate Strong Password", command = generate_password, bg="#1d2b3a", fg="white" ,  font = ("Arial" , 12)).pack(pady = 5) 

root.mainloop()


