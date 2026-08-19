import tkinter as tk


from ui.styles.colors import (
    BG_CARD,
    BORDER,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)


class StatCard(tk.Frame):
    def __init__(self, parent, title, value, icon):
        super().__init__(
            parent,
            bg=BG_CARD,
            highlightbackground=BORDER,
            highlightthickness=1,
        )

        self.grid_propagate(False)

        tk.Label(
            self,
            text=icon,
            bg=BG_CARD,
            font=("Segoe UI", 20),
        ).pack(anchor="w", padx=18, pady=(15, 5))

        tk.Label(
            self,
            text=title,
            bg=BG_CARD,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 10),
        ).pack(anchor="w", padx=18)

        tk.Label(
            self,
            text=value,
            bg=BG_CARD,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 20, "bold"),
        ).pack(anchor="w", padx=18, pady=(2, 15))
