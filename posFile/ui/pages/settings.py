import tkinter as tk
from tkinter import messagebox


class PlaceholderFrame(tk.Frame):
    def __init__(self, parent, controller, title: str):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="white")

        frame = tk.Frame(self, bg="white", padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(
            frame, text=title, font=("Arial", 16, "bold"), bg="white"
        ).pack(pady=20)

        tk.Label(
            frame, text="This page is under development.", font=("Arial", 12), bg="white", fg="grey"
        ).pack(pady=10)

        tk.Button(
            frame,
            text="Back to Dashboard",
            bg="grey",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18,
            command=lambda: self.controller.show_frame("Dashboard"),
        ).pack(pady=20)
