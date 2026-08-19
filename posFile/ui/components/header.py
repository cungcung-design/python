import tkinter as tk


from ui.styles.colors import BG_CARD, BORDER, TEXT_PRIMARY, TEXT_SECONDARY


class Header(tk.Frame):
    def __init__(self, parent):
        super().__init__(
            parent,
            bg=BG_CARD,
            height=65,
            highlightbackground=BORDER,
            highlightthickness=1,
        )

        self.pack_propagate(False)

        tk.Label(
            self,
            text="Smart POS",
            bg=BG_CARD,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 16, "bold"),
        ).pack(side="left", padx=25)

        user_frame = tk.Frame(self, bg=BG_CARD)
        user_frame.pack(side="right", padx=25)

        tk.Label(
            user_frame,
            text="🔔",
            bg=BG_CARD,
            font=("Segoe UI", 14),
        ).pack(side="left", padx=10)

        tk.Label(
            user_frame,
            text="Admin",
            bg=BG_CARD,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left")

        tk.Label(
            user_frame,
            text="▼",
            bg=BG_CARD,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 8),
        ).pack(side="left", padx=5)
