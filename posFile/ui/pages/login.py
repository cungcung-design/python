import tkinter as tk
from tkinter import ttk

from services.auth_service import AuthService
from ui.components.toast import success, error


class LoginFrame(tk.Frame):
    def __init__(self, parent, controller, db, auth_service=None):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        self.auth_service = auth_service or AuthService(db)

        self.configure(bg="lightblue")

        frame = tk.Frame(self, bg="white", padx=30, pady=30)
        frame.pack(expand=True)

        tk.Label(
            frame, text="POS System Login", font=("Segoe UI", 18, "bold"), bg="white"
        ).grid(row=0, column=0, columnspan=2, pady=20)

        tk.Label(frame, text="Username", bg="white", font=("Segoe UI", 11)).grid(
            row=1, column=0, padx=10, pady=10, sticky="e"
        )
        self.entry_username = tk.Entry(frame, font=("Segoe UI", 11))
        self.entry_username.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(frame, text="Password", bg="white", font=("Segoe UI", 11)).grid(
            row=2, column=0, padx=10, pady=10, sticky="e"
        )
        self.entry_password = tk.Entry(frame, show="*", font=("Segoe UI", 11))
        self.entry_password.grid(row=2, column=1, padx=10, pady=10)

        tk.Button(
            frame, text="Login", bg="green", fg="white", width=20, font=("Segoe UI", 11, "bold"), command=self.login
        ).grid(row=3, column=0, padx=10, pady=15)

        tk.Button(
            frame,
            text="Cancel",
            bg="#E5E7EB",
            fg="black",
            width=20,
            font=("Segoe UI", 11, "bold"),
            command=self.cancel_login,
        ).grid(row=3, column=1, padx=10, pady=15)

        self.msg_label = tk.Label(frame, text="", bg="white", font=("Segoe UI", 10))
        self.msg_label.grid(row=4, column=0, columnspan=2)

    def login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if not username or not password:
            error("Please enter username and password")
            return

        user = self.auth_service.authenticate(username, password)

        if not user:
            error("Invalid username or password")
            return

        self.controller.current_user = {
            "id": user["id"],
            "username": user["username"],
            "role": user["role"],
            "staff_id": user.get("staff_id"),
        }

        success("Logged in successfully")
        self.controller.show_frame("Dashboard")

    def cancel_login(self):
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.msg_label.config(text="")
