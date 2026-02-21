import tkinter as tk
from tkinter import ttk


class LoginFrame(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db

        self.configure(bg="lightblue")

        frame = tk.Frame(self, bg="white", padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(
            frame, text="POS System Login", font=("Arial", 16, "bold"), bg="white"
        ).grid(row=0, column=0, columnspan=2, pady=20)

        tk.Label(frame, text="Username", bg="white").grid(
            row=1, column=0, padx=10, pady=10, sticky="e"
        )
        self.entry_username = tk.Entry(frame)
        self.entry_username.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(frame, text="Password", bg="white").grid(
            row=2, column=0, padx=10, pady=10, sticky="e"
        )
        self.entry_password = tk.Entry(frame, show="*")
        self.entry_password.grid(row=2, column=1, padx=10, pady=10)

        tk.Button(
            frame, text="Login", bg="green", fg="white", width=20, command=self.login
        ).grid(row=3, column=0, columnspan=2, pady=15)

        self.msg_label = tk.Label(frame, text="", bg="white")
        self.msg_label.grid(row=4, column=0, columnspan=2)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username == "admin" and password == "123":
            self.controller.show_frame("Dashboard")
        else:
            self.msg_label.config(text="Invalid username or password")
