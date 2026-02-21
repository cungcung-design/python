import tkinter as tk


class DashboardFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        frame = tk.Frame(self, bg="white", padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(
            frame, text="POS SYSTEM DASHBOARD", font=("Arial", 16, "bold"), bg="white"
        ).grid(row=0, column=0, columnspan=2, pady=20)

        tk.Button(
            frame,
            text="POS Sales",font=("Arial", 9, "bold"),
            bg="green",
            fg="white",
            width=30,
            height=2,
            command=lambda: self.controller.show_frame("SalesReport"),
        ).grid(row=1, column=0, columnspan=2, pady=10)

        tk.Label(frame, text="Management", font=("Arial", 12, "bold"), bg="white").grid(
            row=2, column=0, columnspan=2, pady=10
        )

        tk.Button(
            frame,
            text="Category CRUD",
            width=15,
            height=2,
            command=lambda: self.controller.show_frame("Category"),
        ).grid(row=3, column=0, padx=10, pady=10)

        tk.Button(
            frame,
            text="Item CRUD",
            width=15,
            height=2,
            command=lambda: self.controller.show_frame("Item"),
        ).grid(row=3, column=1, padx=10, pady=10)

        tk.Button(
            frame,
            text="Staff CRUD",
            width=15,
            height=2,
            command=lambda: self.controller.show_frame("Staff"),
        ).grid(row=4, column=0, padx=10, pady=10)

        tk.Button(
            frame,
            text="Safe List",
            width=15,
            height=2,
            command=lambda: self.controller.show_frame("SafeList"),
        ).grid(row=4, column=1, padx=10, pady=10)

        tk.Button(
            frame,
            text="Logout",
            bg="red",
            fg="white",
            width=30,
            height=2,
            command=lambda: self.controller.show_frame("Login"),
        ).grid(row=5, column=0, columnspan=2, pady=15)
