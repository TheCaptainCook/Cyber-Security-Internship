import tkinter as tk
from zxcvbn import zxcvbn

def analyze_password(password):
    result = zxcvbn(password)

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

    formatted_text = "\n".join(lines)

    # Directly update the Label
    output.config(text=formatted_text)

# --- Tkinter GUI ---
root = tk.Tk()
root.geometry("600x400")
root.title("Password Strength Checker")

# Input field
entry = tk.Entry(root, show="*", font=("Arial", 14))
entry.pack(pady=10)

# Button to analyze password
btn = tk.Button(root, text="Check Strength", command=lambda: analyze_password(entry.get()))
btn.pack(pady=5)

# Output label (empty at first)
output = tk.Label(root, text="", font=("Arial", 12), justify="left", anchor="w")
output.pack(padx=10, pady=10, fill="both")

root.mainloop()
