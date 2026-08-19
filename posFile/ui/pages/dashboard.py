import tkinter as tk

from services.report_service import ReportService
from ui.components.header import Header
from ui.components.sidebar import Sidebar
from ui.components.toast import success, error
from ui.styles.colors import (
    BG_CARD,
    BG_MAIN,
    BORDER,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)


class DashboardFrame(tk.Frame):
    def __init__(self, parent, controller, report_service):
        super().__init__(parent, bg=BG_MAIN)

        self.controller = controller
        self.report_service = report_service

        # Sidebar
        sidebar = Sidebar(self, controller)
        sidebar.pack(side="left", fill="y")

        # Main area
        main = tk.Frame(self, bg=BG_MAIN)
        main.pack(side="right", fill="both", expand=True)

        # Header
        header = Header(main)
        header.pack(fill="x")

        # Content
        content = tk.Frame(main, bg=BG_MAIN)
        content.pack(fill="both", expand=True, padx=25, pady=25)

        tk.Label(
            content,
            text="Dashboard",
            bg=BG_MAIN,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 22, "bold"),
        ).pack(anchor="w")

        self.user_label = tk.Label(
            content,
            text="",
            bg=BG_MAIN,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 11),
        )
        self.user_label.pack(anchor="w", pady=(3, 20))

        # Statistics row
        stats = tk.Frame(content, bg=BG_MAIN)
        stats.pack(fill="x", pady=(0, 20))
        stats.columnconfigure((0, 1, 2), weight=1)

        self.sales_card = self._make_card(stats, "Today's Sales", "RM 0.00")
        self.sales_card.grid(row=0, column=0, sticky="nsew", padx=5)

        self.transactions_card = self._make_card(stats, "Transactions Today", "0")
        self.transactions_card.grid(row=0, column=1, sticky="nsew", padx=5)

        self.products_card = self._make_card(stats, "Products Total", "0")
        self.products_card.grid(row=0, column=2, sticky="nsew", padx=5)

        # Low stock section
        low_stock_frame = tk.Frame(content, bg=BG_MAIN)
        low_stock_frame.pack(fill="both", expand=True)

        tk.Label(
            low_stock_frame,
            text="Low Stock Products",
            bg=BG_MAIN,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w", pady=(0, 10))

        list_frame = tk.Frame(
            low_stock_frame,
            bg=BG_CARD,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        list_frame.pack(fill="both", expand=True)

        self.low_stock_list = tk.Listbox(
            list_frame,
            bg=BG_CARD,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 10),
            bd=0,
            highlightthickness=0,
            height=8,
        )
        self.low_stock_list.pack(fill="both", expand=True, padx=15, pady=10)

        self.refresh_dashboard()

    def _make_card(self, parent, title, value):
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

        value_label = tk.Label(
            card,
            text=value,
            bg=BG_CARD,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 20, "bold"),
        )
        value_label.pack(anchor="w", padx=20, pady=(0, 15))

        card.value_label = value_label
        return card

    def refresh_dashboard(self):
        try:
            stats = self.report_service.get_dashboard_stats()

            self.sales_card.value_label.config(
                text=f"RM {stats['today_sales']:,.2f}"
            )
            self.transactions_card.value_label.config(
                text=str(stats["today_transactions"])
            )
            self.products_card.value_label.config(
                text=str(stats["total_products"])
            )

            self.low_stock_list.delete(0, tk.END)

            low_stock = self.report_service.get_low_stock_products()

            if not low_stock:
                self.low_stock_list.insert(tk.END, "✓ No low-stock products")
            else:
                for product in low_stock:
                    product_id = product[0]
                    name = product[1]
                    stock = product[2]
                    self.low_stock_list.insert(
                        tk.END,
                        f"#{product_id}  {name}  —  {stock} remaining",
                    )

        except Exception as e:
            print(f"Dashboard refresh failed: {e}")

    def refresh_user(self):
        user = self.controller.current_user

        if user:
            self.user_label.config(
                text=f"Logged in as: {user['username']} ({user['role']})"
            )
