import re

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

def load_banned_passwords(filename):
    with open(filename, "r", encoding="utf-8", errors="ignore") as file:
        return set(line.strip() for line in file)

if __name__ == "__main__":
    print("This file should not be run directly.")
