import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, Toplevel
import random
import string
import itertools
import nltk
from zxcvbn import zxcvbn   # pip install zxcvbn


# ---------- Setup ----------
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

data_storage = []              # Store user data + one generated password
generated_combinations = set() # Store all generated combinations
global_user_value = None       # Last analysed password


# ---------- FUNCTIONS ----------
def warning(code):
    """Show warning messages based on error code."""
    if code == 1:
        messagebox.showwarning("Warning", "No password entered!")
    elif code == 3:
        messagebox.showwarning("Warning", "Password too long (max 33 chars).")
    elif code == 4:
        messagebox.showwarning("Warning", "Password too short (min 8 chars).")


def analyse_password():
    """Ask user for a password and analyse it deeply with zxcvbn."""
    global global_user_value

    received_entry = simpledialog.askstring("Password Input", "Enter your password:", show='*')
    if not received_entry:
        warning(1)

    elif len(received_entry) > 33:
        warning(3)

    elif len(received_entry) < 8:
        warning(4)


    # store value
    global_user_value = received_entry
    result = zxcvbn(global_user_value)

    # Build formatted analysis
    lines = []
    lines.append(f"Password Strength Score: {result['score']}/4")
    lines.append(f"Guesses: {result['guesses']}")
    lines.append(f"Crack Time (offline fast hash): {result['crack_times_display']['offline_fast_hashing_1e10_per_second']}")
    lines.append(f"Crack Time (online throttled): {result['crack_times_display']['online_throttling_100_per_hour']}")

    feedback = result.get("feedback", {})
    if feedback.get("warning"):
        lines.append(f"⚠ Warning: {feedback['warning']}")
    if feedback.get("suggestions"):
        lines.append("Suggestions:")
        for suggestion in feedback["suggestions"]:
            lines.append(f"  - {suggestion}")

    seq = result.get("sequence", [])
    lines.append("Sequence Found:")

    for idx, item in enumerate(seq, start=1):
        lines.append(f"Match {idx}:")
        lines.append(f"  Token: {item.get('token', 'N/A')}")
        lines.append(f"  Matched Word: {item.get('matched_word', 'N/A')}")
        lines.append(f"  Pattern: {item.get('pattern', 'N/A')} (from {item.get('dictionary_name', 'N/A')})")
        lines.append(
            f"  Rank: {item.get('rank', 'N/A')}, "
            f"Guesses: {item.get('guesses', 'N/A')} "
            f"(~10^{item.get('guesses_log10', 0):.2f})"
        )
        lines.append(f"  Position: {item.get('i', '?')}–{item.get('j', '?')}")
        lines.append("-" * 40)

    formatted_text = "\n".join(lines)
    output.config(text=formatted_text)


def generate_password():
    """Open a single dialog to ask for all inputs and generate password."""
    global generated_combinations

    dialog = Toplevel(root)
    dialog.title("Generate Password")
    dialog.geometry("300x300")
    dialog.grab_set()  # Make it modal

    # Labels + Entries
    tk.Label(dialog, text="Enter your name:").pack(pady=5)
    name_entry = tk.Entry(dialog)
    name_entry.pack(pady=5)

    tk.Label(dialog, text="Enter a date (YYYY-MM-DD):").pack(pady=5)
    date_entry = tk.Entry(dialog)
    date_entry.pack(pady=5)

    tk.Label(dialog, text="Enter your pet's name:").pack(pady=5)
    pet_entry = tk.Entry(dialog)
    pet_entry.pack(pady=5)

    def submit():
        nonlocal dialog
        name = name_entry.get().strip()
        date = date_entry.get().strip()
        pet = pet_entry.get().strip()

        if not (name and date and pet):
            messagebox.showwarning("Input Error", "Please fill all fields.")
            return

        # Generate one simple password
        chars = name[:2] + pet[:2] + date[-2:]
        rand_part = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
        generated = chars + rand_part

        # Show result
        messagebox.showinfo("Generated Password", f"Generated Password: {generated}")
        data_storage.append(f"Name: {name}, Date: {date}, Pet: {pet}, Password: {generated}")

        # Generate all possible combinations
        tokens = [name, date, pet]
        generated_combinations = set()
        for r in range(2, len(tokens) + 1):
            for combo in itertools.permutations(tokens, r):
                combined = "".join(combo)
                generated_combinations.add(combined)
                generated_combinations.add(combined.lower())
                generated_combinations.add(combined.upper())
                generated_combinations.add(combined.capitalize())

        messagebox.showinfo("Combinations Ready",
                            f"Generated {len(generated_combinations)} password combinations.\nUse 'Export Data' to save them.")

        dialog.destroy()

    tk.Button(dialog, text="Generate", command=submit).pack(pady=15)


def export_data():
    """Export collected data and combinations to a text file."""
    if not data_storage and not generated_combinations:
        messagebox.showwarning("Export", "No data to export!")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("==== USER INPUT DATA ====\n")
            f.write("\n".join(data_storage))
            f.write("\n\n==== GENERATED COMBINATIONS ====\n")
            f.write("\n".join(sorted(generated_combinations)))
        messagebox.showinfo("Export", f"Data exported to {file_path}")


def exit_program():
    """Exit the application."""
    root.destroy()


# ---------- MAIN APP ----------
root = tk.Tk()
root.title("Password Tool")
root.geometry("700x600")

btn1 = tk.Button(root, text="Analyse Password", command=analyse_password, width=25)
btn1.pack(pady=10)

btn2 = tk.Button(root, text="Generate Password", command=generate_password, width=25)
btn2.pack(pady=10)

btn3 = tk.Button(root, text="Export Data", command=export_data, width=25)
btn3.pack(pady=10)

btn4 = tk.Button(root, text="Exit", command=exit_program, width=25)
btn4.pack(pady=10)

# Output label for password analysis
output = tk.Label(root, text="", justify="left", anchor="w", font=("Courier", 10), wraplength=650)
output.pack(padx=10, pady=10, fill="both", expand=True)

root.mainloop()
