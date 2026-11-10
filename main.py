
import tkinter as tk
from tkinter import messagebox
from scanner import scan_url
from datetime import datetime

# Main window
root = tk.Tk()
root.title("PhishGuard - URL Security Scanner")
root.geometry("750x700")
root.configure(bg="#101827")
root.resizable(False, False)

history = []

# Colors
BG = "#101827"
CARD = "#1E293B"
WHITE = "#FFFFFF"
BLUE = "#38BDF8"
GREEN = "#22C55E"
YELLOW = "#FACC15"
RED = "#EF4444"

# Heading
title = tk.Label(
    root,
    text="PHISHGUARD",
    font=("Arial", 27, "bold"),
    bg=BG,
    fg=BLUE
)
title.pack(pady=(20, 5))

subtitle = tk.Label(
    root,
    text="Python-Based Phishing URL Awareness Checker",
    font=("Arial", 11),
    bg=BG,
    fg=WHITE
)
subtitle.pack(pady=5)

# Main card
card = tk.Frame(root, bg=CARD, padx=25, pady=20)
card.pack(padx=30, pady=20, fill="x")

tk.Label(
    card,
    text="Enter Website URL",
    font=("Arial", 13, "bold"),
    bg=CARD,
    fg=WHITE
).pack(anchor="w")

url_entry = tk.Entry(
    card,
    font=("Arial", 13),
    bg="#334155",
    fg=WHITE,
    insertbackground=WHITE,
    relief="flat"
)
url_entry.pack(fill="x", ipady=12, pady=12)

# Result area
result_frame = tk.Frame(root, bg=CARD, padx=20, pady=20)
result_frame.pack(padx=30, fill="both", expand=True)

tk.Label(
    result_frame,
    text="SCAN RESULTS",
    font=("Arial", 15, "bold"),
    bg=CARD,
    fg=BLUE
).pack(anchor="w")

risk_label = tk.Label(
    result_frame,
    text="Waiting for scan...",
    font=("Arial", 20, "bold"),
    bg=CARD,
    fg=WHITE
)
risk_label.pack(pady=12)

score_label = tk.Label(
    result_frame,
    text="Risk Score: -- / 100",
    font=("Arial", 13),
    bg=CARD,
    fg=WHITE
)
score_label.pack()

reason_label = tk.Label(
    result_frame,
    text="Scan a URL to see the analysis.",
    font=("Arial", 11),
    bg=CARD,
    fg=WHITE,
    justify="left",
    wraplength=620
)
reason_label.pack(pady=15, anchor="w")

recommend_label = tk.Label(
    result_frame,
    text="",
    font=("Arial", 11, "bold"),
    bg=CARD,
    fg=YELLOW,
    justify="left",
    wraplength=620
)
recommend_label.pack(anchor="w", pady=5)


def scan():

    url = url_entry.get().strip()

    if not url:
        messagebox.showwarning(
            "Missing URL",
            "Please enter a website URL."
        )
        return

    result = scan_url(url)

    risk = result["risk"]

    if risk == "LOW RISK":
        color = GREEN
    elif risk == "MEDIUM RISK":
        color = YELLOW
    else:
        color = RED

    risk_label.config(
        text=risk,
        fg=color
    )

    score_label.config(
        text=f"Risk Score: {result['score']} / 100"
    )

    reasons = "\n".join(
        "• " + reason for reason in result["reasons"]
    )

    reason_label.config(
        text="Detection Details:\n\n" + reasons
    )

    recommend_label.config(
        text="Recommendation:\n" + result["recommendation"]
    )

    history.append(
        f"{datetime.now().strftime('%H:%M:%S')} - {url} - {risk}"
    )

    history_label.config(
        text="\n".join(history[-5:])
    )


def clear():

    url_entry.delete(0, tk.END)

    risk_label.config(
        text="Waiting for scan...",
        fg=WHITE
    )

    score_label.config(text="Risk Score: -- / 100")

    reason_label.config(
        text="Scan a URL to see the analysis."
    )

    recommend_label.config(text="")


# Buttons
button_frame = tk.Frame(root, bg=BG)
button_frame.pack(pady=12)

scan_button = tk.Button(
    button_frame,
    text="SCAN URL",
    font=("Arial", 12, "bold"),
    bg=BLUE,
    fg="#101827",
    width=17,
    relief="flat",
    cursor="hand2",
    command=scan
)
scan_button.pack(side="left", padx=10, ipady=8)

clear_button = tk.Button(
    button_frame,
    text="CLEAR",
    font=("Arial", 12, "bold"),
    bg="#475569",
    fg=WHITE,
    width=17,
    relief="flat",
    cursor="hand2",
    command=clear
)
clear_button.pack(side="left", padx=10, ipady=8)

# Scan history
history_frame = tk.Frame(root, bg=BG)
history_frame.pack(padx=30, pady=5, fill="x")

tk.Label(
    history_frame,
    text="RECENT SCANS",
    font=("Arial", 11, "bold"),
    bg=BG,
    fg=BLUE
).pack(anchor="w")

history_label = tk.Label(
    history_frame,
    text="No scans yet.",
    font=("Arial", 9),
    bg=BG,
    fg=WHITE,
    justify="left"
)
history_label.pack(anchor="w", pady=5)

# Footer
tk.Label(
    root,
    text="Educational tool only | PhishGuard Project",
    font=("Arial", 9),
    bg=BG,
    fg="#94A3B8"
).pack(pady=10)

root.mainloop()
