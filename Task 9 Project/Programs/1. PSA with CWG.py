#.Analyze user password using zxcvbn or custom entropy calculations.
#b.Allow user inputs (name, date, pet) to generate a custom wordlist.
#c.Include common patterns like leetspeak, append years.
#d.Export in .txt format for cracking tools.
#e.Add GUI with tkinter or CLI interface.
import random
import string
import tkinter as tk
import tkinter.messagebox
from zxcvbn import zxcvbn

# Declare a global variable
global_user_value = ""

# Word associations for characters
associations = {
    # Lowercase letters
    **{c: w for c, w in zip(
        "abcdefghijklmnopqrstuvwxyz",
        ["apple","ball","cat","dog","elephant","fish","goat","hat","ice","jungle",
         "kite","lion","monkey","nest","orange","pen","queen","rat","sun","tree",
         "umbrella","vase","wolf","xylophone","yarn","zebra"]
    )},

    # Uppercase letters
    **{c.upper(): w.capitalize() for c, w in zip(
        "abcdefghijklmnopqrstuvwxyz",
        ["apple","ball","cat","dog","elephant","fish","goat","hat","ice","jungle",
         "kite","lion","monkey","nest","orange","pen","queen","rat","sun","tree",
         "umbrella","vase","wolf","xylophone","yarn","zebra"]
    )},

    # Digits
    **{c: w for c, w in zip(
        "0123456789",
        ["zero","one","two","three","four","five","six","seven","eight","nine"]
    )},

    # Common special characters
    "!": "bang", "@": "at", "#": "hash", "$": "dollar", "%": "percent",
    "^": "caret", "&": "and", "*": "star", "(": "open-paren", ")": "close-paren",
    "-": "dash", "_": "underscore", "=": "equal", "+": "plus",
    "?": "question", "/": "slash", ".": "dot", ",": "comma", ";": "semicolon",
    ":": "colon", "'": "quote", '"': "double-quote", "[": "open-bracket", "]": "close-bracket",
    "{": "open-brace", "}": "close-brace", "<": "less-than", ">": "greater-than",
    "|": "pipe", "~": "tilde", "`": "backtick"
}


def generate_password():
    global global_user_value
    length = length_slider.get()  # Get value from slider
    characters = string.ascii_letters + string.digits + string.punctuation
    global_user_value = ''.join(random.choice(characters) for i in range(int(length)))
    entry.delete(0, tk.END)     # clears the entry box
    entry.insert(0, global_user_value)

    clear_all_data(1)


def easy_way_to_remember():
    word_pairs = []
    for pair in password_with_associations(global_user_value):
        word_pairs.append(pair)

    format_text = "Easier ways to remember Password\n\n" + "\n".join(word_pairs)
    output_associations.config(text=format_text)

    clear_all_data(2)


def password_with_associations(password):
    return [f"{ch} → {associations.get(ch, 'unknown')}" for ch in password]

def copy_password():
    # Copy the current password to clipboard
    root.clipboard_clear()
    root.clipboard_append(entry.get())
    root.update()
    warning(2)


def analyze_password(received_entry):
    global global_user_value
    if not received_entry:
        warning(1)
    elif len(received_entry) > 33:
        warning(3)
    else:
        if len(received_entry) < 8:
            warning(4)
        global_user_value = received_entry
        result = zxcvbn(global_user_value)
        # Build formatted text (but don't return it, put directly in Label)
        lines = []
        lines.append(f"Password Strength Score: {result['score']}/4")
        lines.append(f"Guesses: {result['guesses']}")
        lines.append(
            f"Crack Time (offline fast hash): {result['crack_times_display']['offline_fast_hashing_1e10_per_second']}")
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

        # Directly update the Label
        output.config(text=formatted_text)

        clear_all_data(3)


def warning(received_warning):  #bad -icon value "success": must be error, info, question, or warning
    if received_warning == 1:
        tkinter.messagebox.showinfo("Oops!!", "Password field cannot be empty", icon="error")
    elif received_warning == 2:
        tkinter.messagebox.showinfo("Success", "Password has been copied to clipboard", icon="info")
    elif received_warning == 3:
        tkinter.messagebox.showerror("Length Error", "Password above 32 characters are not supported", icon="error")
    elif received_warning == 4:
        tkinter.messagebox.showinfo("Vital Information", "Passwords below 8 characters is not secure", icon="info")
    elif received_warning == 9:
        exit_warning = tkinter.messagebox.askyesno("Warning", "Do you want to Exit?", icon="warning")
        if exit_warning:
            root.destroy()
    elif received_warning == 10:
        personalised_credits = []
        personalised_credits.append("Made by")
        personalised_credits.append("Sheikh Masem Mandal")
        personalised_credits.append("Completed in 2 days")
        personalised_credits.append("During Cyber Security Internship")
        personalised_credits.append("Email: masem1996@gmail.com")
        personalised_credits.append("Phone: +918550901610 ")
        personalised_credits.append("Github - TheCaptainCook ")
        personalised_credits.append("Github Link - https://github.com/thecaptaincook")
        personalised_credits.append("LinkedIn Link = https://www.linkedin.com/in/masemmandal/")
        format_credits = "\n".join(personalised_credits)
        tkinter.messagebox.showinfo("Credits", format_credits, icon="info")

def clear_all_data(custom_clear_action_flag):
    if custom_clear_action_flag==0:
        output.config(text="")
        output_associations.config(text="")
        entry.delete(0, tk.END)
    elif custom_clear_action_flag==1:
        output.config(text="")
        output_associations.config(text="")
    elif custom_clear_action_flag==2:
        output.config(text="")
    elif custom_clear_action_flag==3:
        output_associations.config(text="")

#Main Program
# --- Tkinter GUI ---
root = tk.Tk()
root.title("Password Strength Checker")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry(f"{screen_width}x{screen_height}")


# Label
label = tk.Label(root, text="Enter a value:")
label.pack(pady=5)


# Entry widget
entry = tk.Entry(root)
entry.pack(pady=5)


# Slider for password length
length_slider = tk.Scale(root, from_=4, to=32, orient=tk.HORIZONTAL, label="Password Length")
length_slider.set(8)  # Default value
length_slider.pack(pady=10)


# --- Top Row ---
top_frame = tk.Frame(root)
top_frame.pack(pady=5)

gen_pass_btn = tk.Button(top_frame, text="Generate Password", command=generate_password)
gen_pass_btn.pack(side="left", padx=5, expand=True, fill="x")

check_strength_btn = tk.Button(top_frame, text="Check Strength", command=lambda: analyze_password(entry.get()))
check_strength_btn.pack(side="left", padx=5, expand=True, fill="x")

easy_remember_btn = tk.Button(top_frame, text="Easy Way to Remember", command=easy_way_to_remember)
easy_remember_btn.pack(side="left", padx=5, expand=True, fill="x")

# --- Bottom Row ---
bottom_frame = tk.Frame(root)
bottom_frame.pack(pady=5)

copy_btn = tk.Button(bottom_frame, text="Copy Password", command=copy_password)
copy_btn.pack(side="left", padx=5, expand=True, fill="x")

exit_btn = tk.Button(bottom_frame, text="Exit Program", command=lambda: warning(9))
exit_btn.pack(side="left", padx=5, expand=True, fill="x")

credits_btn = tk.Button(bottom_frame, text="Credits", command=lambda: warning(10))
credits_btn.pack(side="left", padx=5, expand=True, fill="x")

#Quick way to remember password
output_associations = tk.Label(root, text="", font=("Arial", 12), justify="left", anchor="w")
output_associations.pack(padx=10, pady=10, fill="both")

# Output label (empty at first)
output = tk.Label(root, text="", font=("Arial", 12), justify="left", anchor="w")
output.pack(padx=10, pady=10, fill="both")

#clear Screen
clear_btn = tk.Button(root, text="Clear All Data", command=lambda :clear_all_data(0), justify="center")
clear_btn.pack(side="bottom", padx=10, pady=10, fill="both")


# Main Program Starts Here
root.mainloop()