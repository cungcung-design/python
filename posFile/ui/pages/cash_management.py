import tkinter as tk
from tkinter import messagebox

from services.cash_service import CashService

from ui.styles.colors import (
    BG_CARD,
    BG_MAIN,
    BORDER,
    PRIMARY,
    PRIMARY_HOVER,
    SUCCESS,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)
from ui.components.toast import success, error, warning


class CashManagementFrame(tk.Frame):
    def __init__(self, parent, controller, db, cash_service=None):
        super().__init__(parent, bg=BG_MAIN)

        self.controller = controller
        self.db = db
        self.cash_service = cash_service

        self.create_ui()
        self.load_register()

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------

    def create_ui(self):
        header = tk.Frame(self, bg=BG_CARD, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="Cash Register",
            bg=BG_CARD,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 22, "bold"),
        ).pack(side="left", padx=25, pady=18)

        tk.Button(
            header,
            text="← Dashboard",
            command=lambda: self.controller.show_frame("Dashboard"),
            bg=BG_CARD,
            fg=TEXT_PRIMARY,
            relief="flat",
            bd=0,
            cursor="hand2",
        ).pack(side="right", padx=25)

        body = tk.Frame(self, bg=BG_MAIN)
        body.pack(fill="both", expand=True, padx=30, pady=30)

        card = tk.Frame(body, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="both", expand=True, padx=20, pady=20)

        inner = tk.Frame(card, bg=BG_CARD)
        inner.pack(fill="both", expand=True, padx=40, pady=40)

        self.status_label = tk.Label(
            inner,
            text="Register Closed",
            bg=BG_CARD,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 18, "bold"),
        )
        self.status_label.pack(pady=(0, 20))

        self.summary_label = tk.Label(
            inner,
            text="No register is currently open.",
            bg=BG_CARD,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 11),
            justify="center",
        )
        self.summary_label.pack(pady=(0, 20))

        amount_frame = tk.Frame(inner, bg=BG_CARD)
        amount_frame.pack(pady=(0, 20))

        tk.Label(
            amount_frame,
            text="Amount (RM)",
            bg=BG_CARD,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(0, 5))

        self.amount_entry = tk.Entry(amount_frame, font=("Segoe UI", 14), justify="center")
        self.amount_entry.pack(fill="x", ipady=8)

        buttons = tk.Frame(inner, bg=BG_CARD)
        buttons.pack(pady=(10, 0))

        self.open_button = tk.Button(
            buttons,
            text="Open Register",
            command=self.open_register,
            bg=SUCCESS,
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=25,
            pady=10,
            font=("Segoe UI", 11, "bold"),
        )
        self.open_button.pack(side="left", padx=5)

        self.close_button = tk.Button(
            buttons,
            text="Close Register",
            command=self.close_register,
            bg="#EF4444",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=25,
            pady=10,
            font=("Segoe UI", 11, "bold"),
            state="disabled",
        )
        self.close_button.pack(side="left", padx=5)

    # ---------------------------------------------------------
    # Register operations
    # ---------------------------------------------------------

    def load_register(self):
        user = self.controller.current_user
        if not user:
            return

        user_id = user["id"]
        staff_id = user.get("staff_id")

        register = self.cash_service.get_open_register(staff_id)

        if register:
            self.status_label.config(text="🟢 Register Open")
            self.open_button.config(state="disabled")
            self.close_button.config(state="normal")

            expected = self.cash_service.calculate_expected_cash(user_id, staff_id)
            self.summary_label.config(
                text=(
                    f"Opening Cash: RM {float(register[1]):,.2f}\n\n"
                    f"Expected Cash: RM {expected:,.2f}"
                )
            )
        else:
            self.status_label.config(text="🔴 Register Closed")
            self.open_button.config(state="normal")
            self.close_button.config(state="disabled")
            self.summary_label.config(text="No register is currently open.")

    def open_register(self):
        try:
            amount = float(self.amount_entry.get())
            if amount < 0:
                raise ValueError
        except ValueError:
            error("Enter a valid opening cash amount.")
            return

        user = self.controller.current_user
        staff_id = user.get("staff_id")
        user_id = user.get("id") if user else None
        register = self.cash_service.open_register(staff_id, amount, user_id=user_id)

        if not register:
            warning("This cashier already has an open register.")
            return

        self.amount_entry.delete(0, tk.END)
        self.load_register()
        success(f"Register opened with RM {amount:,.2f}")

    def close_register(self):
        try:
            actual = float(self.amount_entry.get())
            if actual < 0:
                raise ValueError
        except ValueError:
            error("Enter the actual cash counted.")
            return

        user = self.controller.current_user
        user_id = user["id"]
        staff_id = user.get("staff_id")
        result = self.cash_service.close_register(user_id, staff_id, actual)

        if not result:
            return

        difference = result["difference"]

        if difference == 0:
            message = "Register balanced perfectly."
        elif difference > 0:
            message = f"Cash over by RM {difference:,.2f}"
        else:
            message = f"Cash short by RM {abs(difference):,.2f}"

        success(
            f"Register closed.\n"
            f"Expected: RM {result['expected']:,.2f}\n"
            f"Actual: RM {result['actual']:,.2f}\n"
            f"Difference: RM {difference:,.2f}\n\n"
            f"{message}"
        )

        self.amount_entry.delete(0, tk.END)
        self.load_register()
