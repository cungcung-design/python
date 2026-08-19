import tkinter as tk
from tkinter import ttk


def apply_treeview_style(tree: ttk.Treeview):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
    style.configure(
        "Treeview",
        background="#f0f0f0",
        fieldbackground="#f0f0f0",
        font=("Arial", 10),
        rowheight=25,
        foreground="black",
        bordercolor="lightblue",
        borderwidth=2,
        highlightthickness=0,
    )


def style_button(btn: tk.Button, bg: str = "lightgrey", fg: str = "black"):
    btn.config(bg=bg, fg=fg, font=("Arial", 10, "bold"))
