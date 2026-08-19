import tkinter as tk


from ui.styles.colors import (
    BG_SIDEBAR,
    BG_SIDEBAR_HOVER,
    TEXT_LIGHT,
    TEXT_SECONDARY,
)


class Sidebar(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_SIDEBAR, width=220)

        self.controller = controller

        self.pack_propagate(False)

        # Logo
        logo_frame = tk.Frame(self, bg=BG_SIDEBAR)
        logo_frame.pack(fill="x", padx=20, pady=(25, 30))

        tk.Label(
            logo_frame,
            text="🏪",
            bg=BG_SIDEBAR,
            fg=TEXT_LIGHT,
            font=("Segoe UI", 22),
        ).pack(side="left")

        tk.Label(
            logo_frame,
            text="Smart POS",
            bg=BG_SIDEBAR,
            fg=TEXT_LIGHT,
            font=("Segoe UI", 16, "bold"),
        ).pack(side="left", padx=8)

        # Navigation
        self.create_button("📊  Dashboard", "Dashboard")
        self.create_button("🛒  POS", "POS")
        self.create_button("📦  Products", "Item")
        self.create_button("📋  Inventory", "Inventory")
        self.create_button("🏷  Categories", "Category")
        self.create_button("👥  Staff", "Staff")
        self.create_button("💰  Sales", "SalesReport")
        self.create_button("💵  Cash Management", "CashManagement")
        self.create_button("📝  Audit Logs", "Audit")

        self.create_button("ℹ  About", None)

        spacer = tk.Frame(self, bg=BG_SIDEBAR)
        spacer.pack(fill="both", expand=True)

        self.create_button("⚙  Settings", "Settings")
        self.create_button("🚪  Logout", "Login")

    def create_button(self, text, frame_name):
        button = tk.Button(
            self,
            text=text,
            anchor="w",
            bd=0,
            relief="flat",
            bg=BG_SIDEBAR,
            fg=TEXT_SECONDARY if frame_name is None else TEXT_LIGHT,
            activebackground=BG_SIDEBAR_HOVER,
            activeforeground=TEXT_LIGHT,
            font=("Segoe UI", 10),
            padx=20,
            pady=12,
            cursor="hand2",
            command=lambda: self.navigate(frame_name) if frame_name else self.controller.show_about(),
        )

        button.pack(fill="x", padx=10, pady=2)

    def navigate(self, frame_name):
        if frame_name:
            self.controller.show_frame(frame_name)
