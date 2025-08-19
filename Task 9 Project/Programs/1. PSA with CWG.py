#.Analyze user password using zxcvbn or custom entropy calculations.
#b.Allow user inputs (name, date, pet) to generate a custom wordlist.
#c.Include common patterns like leetspeak, append years.
#d.Export in .txt format for cracking tools.
#e.Add GUI with tkinter or CLI interface.
import tkinter as tk
import tkinter.messagebox
from tkinter.messagebox import askyesno

from torch.distributions.constraints import boolean
from zxcvbn import zxcvbn

def analyze_password(passwd):
    result = zxcvbn(passwd)

    # Build formatted text (but don't return it, put directly in Label)
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
    lines.append(f"Sequence Found:")
    for idx, item in enumerate(seq, start=1):
        lines.append(f"Match {idx}:")
        lines.append(f"  Token: {item['token']}")
        lines.append(f"  Matched Word: {item['matched_word']}")
        lines.append(f"  Pattern: {item['pattern']} (from {item['dictionary_name']})")
        lines.append(f"  Rank: {item['rank']}, Guesses: {item['guesses']} (~10^{item['guesses_log10']:.2f})")
        lines.append(f"  Position: {item['i']}–{item['j']}")
        lines.append("-" * 40)

    formatted_text = "\n".join(lines)

    # Directly update the Label
    output.config(text=formatted_text)

def exit_program_confirmation():
    make_sure = tkinter.messagebox.askyesno("Exit", "Are you sure you want to exit?", icon="warning")
    if make_sure:
        root.destroy()
    else :
        root.mainloop()


    root.destroy()

# --- Tkinter GUI ---
root = tk.Tk()
root.geometry("600x400")
root.title("Password Strength Checker")

# Input field
#entry = tk.Entry(root, show="*", font=("Arial", 14))
#entry = tk.Entry(root, font=("Arial", 20), justify="center")
#entry = tk.Entry(root, font=("Arial", 14), show="*"); entry.bind("<Double-Button-1>", lambda e: entry.config(show="" if entry.cget("show")=="*" else "*"))
entry = tk.Entry(root, font=("Arial", 14), show="*"); entry.bind("<Double-Button-1>", lambda e: entry.config(show="" if entry.cget("show")=="*" else "*")); entry.bind("<Enter>", lambda e: entry.config(show="")); entry.bind("<Leave>", lambda e: entry.config(show="*"))
entry.pack(pady=10)

# Button to analyze password
btn = tk.Button(root, text="Check Strength", command=lambda: analyze_password(entry.get()))
btn.pack(pady=5)

# Output label (empty at first)
output = tk.Label(root, text="", font=("Arial", 12), justify="left", anchor="w")
output.pack(padx=10, pady=10, fill="both")

#button to exit program
#exit_button = tk.Button(root, text="Exit", command=exit_program_confirmation)
#exit_button.pack(padx=10, pady=10)
#root.mainloop()


root.mainloop()