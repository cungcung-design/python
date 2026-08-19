import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from services.report_service import ReportService

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
from ui.components.toast import error


class SalesReportFrame(tk.Frame):
    def __init__(self, parent, controller, db):
        super().__init__(parent, bg=BG_MAIN)

        self.controller = controller
        self.db = db
        self.report_service = ReportService(db)

        # Header
        header = tk.Frame(self, bg=BG_CARD, height=65)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="Sales & Analytics",
            bg=BG_CARD,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 20, "bold"),
        ).pack(side="left", padx=25)

        tk.Button(
            header,
            text="← Dashboard",
            command=lambda: controller.show_frame("Dashboard"),
            bg=BG_CARD,
            fg=TEXT_PRIMARY,
            relief="flat",
            bd=0,
            cursor="hand2",
        ).pack(side="right", padx=25)

        # Content
        content = tk.Frame(self, bg=BG_MAIN)
        content.pack(fill="both", expand=True, padx=20, pady=20)

        # Stats cards
        stats = tk.Frame(content, bg=BG_MAIN)
        stats.pack(fill="x", pady=(0, 20))
        stats.columnconfigure((0, 1), weight=1)

        self.sales_card = self._make_stat_card(stats, "Today's Sales", "RM 0.00", 0)
        self.sales_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        self.transactions_card = self._make_stat_card(stats, "Transactions", "0", 1)
        self.transactions_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        # Sales history
        history_frame = tk.Frame(content, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1)
        history_frame.pack(fill="both", expand=True, pady=(0, 20))

        tk.Label(
            history_frame,
            text="Sales History",
            bg=BG_CARD,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w", padx=20, pady=(20, 10))

        self.sales_tree = ttk.Treeview(
            history_frame,
            columns=("Date", "Sales", "Transactions"),
            show="headings",
            height=8,
        )
        self.sales_tree.heading("Date", text="Date")
        self.sales_tree.heading("Sales", text="Sales")
        self.sales_tree.heading("Transactions", text="Transactions")
        self.sales_tree.column("Date", width=150, anchor="center")
        self.sales_tree.column("Sales", width=150, anchor="e")
        self.sales_tree.column("Transactions", width=150, anchor="center")

        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.sales_tree.yview)
        self.sales_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.sales_tree.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=(0, 20))

        # Best sellers
        best_frame = tk.Frame(content, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1)
        best_frame.pack(fill="both", expand=True)

        tk.Label(
            best_frame,
            text="Best Selling Products",
            bg=BG_CARD,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w", padx=20, pady=(20, 10))

        self.best_tree = ttk.Treeview(
            best_frame,
            columns=("Product", "Units Sold", "Revenue"),
            show="headings",
            height=8,
        )
        self.best_tree.heading("Product", text="Product")
        self.best_tree.heading("Units Sold", text="Units Sold")
        self.best_tree.heading("Revenue", text="Revenue")
        self.best_tree.column("Product", width=200, anchor="w")
        self.best_tree.column("Units Sold", width=120, anchor="center")
        self.best_tree.column("Revenue", width=120, anchor="e")

        best_scroll = ttk.Scrollbar(best_frame, orient="vertical", command=self.best_tree.yview)
        self.best_tree.configure(yscrollcommand=best_scroll.set)
        best_scroll.pack(side="right", fill="y")
        self.best_tree.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=(0, 20))

        self.load_reports()

    def _make_stat_card(self, parent, title, value, col):
        card = tk.Frame(
            parent,
            bg=BG_CARD,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        card.pack_propagate(False)
        card.configure(height=100)

        tk.Label(
            card,
            text=title,
            bg=BG_CARD,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 10),
        ).pack(anchor="w", padx=20, pady=(15, 5))

        label = tk.Label(
            card,
            text=value,
            bg=BG_CARD,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 20, "bold"),
        )
        label.pack(anchor="w", padx=20, pady=(0, 15))

        card.value_label = label
        return card

    def load_reports(self):
        try:
            sales, transactions = self.report_service.get_today_summary()
            self.sales_card.value_label.config(text=f"RM {float(sales):,.2f}")
            self.transactions_card.value_label.config(text=str(transactions))

            # Sales history
            for item in self.sales_tree.get_children():
                self.sales_tree.delete(item)

            history = self.report_service.get_sales_summary()
            for row in history:
                self.sales_tree.insert(
                    "",
                    "end",
                    values=(
                        row[0],
                        f"RM {float(row[1]):,.2f}",
                        row[2],
                    ),
                )

            # Best sellers
            for item in self.best_tree.get_children():
                self.best_tree.delete(item)

            products = self.report_service.get_best_selling_products()
            for row in products:
                self.best_tree.insert(
                    "",
                    "end",
                    values=(
                        row[0],
                        row[1],
                        f"RM {float(row[2]):,.2f}",
                    ),
                )
        except Exception:
            print(f"Reports error: {e}")
            error("Something went wrong. Please try again.")
