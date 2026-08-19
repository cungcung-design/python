import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from services.sales_service import SalesService

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


class POSFrame(tk.Frame):
    def __init__(self, parent, controller, db, sales_service=None):
        super().__init__(parent, bg=BG_MAIN)

        self.controller = controller
        self.db = db
        self.sales_service = sales_service

        self.cart = {}
        self.payment_method = tk.StringVar(value="Cash")
        self._all_products = []
        self._best_seller_ids = set()

        self.build_ui()
        self.after(0, self.load_products)

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------

    def build_ui(self):
        header = tk.Frame(self, bg=BG_CARD, height=65)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="Point of Sale",
            bg=BG_CARD,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 20, "bold"),
        ).pack(side="left", padx=25)

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

        content = tk.Frame(self, bg=BG_MAIN)
        content.pack(fill="both", expand=True, padx=20, pady=20)

        # LEFT - Products
        left = tk.Frame(content, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(
            left,
            text="Products",
            bg=BG_CARD,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w", padx=20, pady=(20, 10))

        # Best sellers
        best_frame = tk.Frame(left, bg=BG_CARD)
        best_frame.pack(fill="x", padx=20, pady=(0, 10))

        tk.Label(
            best_frame,
            text="Best Sellers",
            bg=BG_CARD,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w")

        self.best_frame = tk.Frame(best_frame, bg=BG_CARD)
        self.best_frame.pack(fill="x", pady=(5, 0))

        # Search
        search_frame = tk.Frame(left, bg=BG_CARD)
        search_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.search_products)

        search = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Segoe UI", 10),
        )
        search.pack(fill="x", ipady=5)

        # Product grid
        self.products_frame = tk.Frame(left, bg=BG_CARD)
        self.products_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        # RIGHT - Cart
        right = tk.Frame(content, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1)
        right.pack(side="right", fill="both", expand=True, padx=(10, 0))

        tk.Label(
            right,
            text="Current Order",
            bg=BG_CARD,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w", padx=20, pady=(20, 10))

        # Cart items
        self.cart_tree = ttk.Treeview(
            right,
            columns=("Name", "Qty", "Total"),
            show="headings",
            height=15,
        )
        self.cart_tree.heading("Name", text="Item")
        self.cart_tree.heading("Qty", text="Qty")
        self.cart_tree.heading("Total", text="Total")
        self.cart_tree.column("Name", width=180)
        self.cart_tree.column("Qty", width=60, anchor="center")
        self.cart_tree.column("Total", width=100, anchor="e")

        cart_scroll = ttk.Scrollbar(right, orient="vertical", command=self.cart_tree.yview)
        self.cart_tree.configure(yscrollcommand=cart_scroll.set)
        cart_scroll.pack(side="right", fill="y")
        self.cart_tree.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=(0, 10))

        # Cart controls
        cart_controls = tk.Frame(right, bg=BG_CARD)
        cart_controls.pack(fill="x", padx=20, pady=5)

        tk.Button(
            cart_controls,
            text="Remove",
            command=self.remove_selected,
            bg=BG_MAIN,
            relief="flat",
        ).pack(side="left", padx=2)

        tk.Button(
            cart_controls,
            text="Clear",
            command=self.clear_cart,
            bg=BG_MAIN,
            relief="flat",
        ).pack(side="right", padx=2)

        # Totals
        totals = tk.Frame(right, bg=BG_CARD)
        totals.pack(fill="x", padx=20, pady=10)

        self.subtotal_label = self.add_total_row(totals, "Subtotal", "RM 0.00")
        self.discount_label = self.add_total_row(totals, "Discount", "RM 0.00")
        self.tax_label = self.add_total_row(totals, "Tax", "RM 0.00")
        self.total_label = self.add_total_row(totals, "Total", "RM 0.00", bold=True)

        # Payment method
        payment = tk.Frame(right, bg=BG_CARD)
        payment.pack(fill="x", padx=20, pady=10)

        tk.Label(payment, text="Payment:", bg=BG_CARD, fg=TEXT_SECONDARY, font=("Segoe UI", 10)).pack(
            side="left"
        )

        tk.Radiobutton(
            payment,
            text="Cash",
            variable=self.payment_method,
            value="Cash",
            bg="white",
        ).pack(side="left", padx=10)

        tk.Radiobutton(
            payment,
            text="Card",
            variable=self.payment_method,
            value="Card",
            bg="white",
        ).pack(side="left")

        # Checkout
        tk.Button(
            right,
            text="COMPLETE SALE",
            font=("Segoe UI", 12, "bold"),
            height=2,
            command=self.checkout,
            bg=SUCCESS,
            fg="white",
            relief="flat",
            cursor="hand2",
        ).pack(fill="x", padx=20, pady=15)

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def add_total_row(self, parent, title, value, bold=False):
        font = ("Segoe UI", 11, "bold" if bold else "normal")
        row = tk.Frame(parent, bg=BG_CARD)
        row.pack(fill="x", pady=3)

        tk.Label(row, text=title, font=font, bg=BG_CARD).pack(side="left")
        label = tk.Label(row, text=value, font=font, bg=BG_CARD)
        label.pack(side="right")
        return label

    # ---------------------------------------------------------
    # Products
    # ---------------------------------------------------------

    def load_products(self):
        self.after(0, self._do_load_products)

    def _do_load_products(self):
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        try:
            self._all_products = self.db.fetch_all(
                """
                SELECT id, name, price, stock_quantity
                FROM items
                ORDER BY name
                """
            )
            self._render_products(self._all_products)
            self._load_best_sellers()
        except Exception:
            print(f"Database error: {e}")
            error("Something went wrong. Please try again.")

    def _render_products(self, products):
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        for product in products:
            self.create_product_button(product)

    def create_product_button(self, product):
        product_id = product[0]
        name = product[1]
        price = float(product[2])
        stock = int(product[3])

        state = "disabled" if stock <= 0 else "normal"

        button = tk.Button(
            self.products_frame,
            text=f"{name}\nRM {price:,.2f}",
            font=("Segoe UI", 11, "bold"),
            width=18,
            height=4,
            state=state,
            command=lambda p=product: self.add_to_cart(p),
        )
        button.pack(side="left", padx=8, pady=8)

    def search_products(self, event=None):
        search = self.search_var.get().strip()

        products = list(self._all_products)

        if search:
            products = [
                p for p in products
                if search.lower() in str(p[1]).lower() or search.lower() in str(p[3]).lower()
            ]

        self._render_products(products)

    # ---------------------------------------------------------
    # Best sellers
    # ---------------------------------------------------------

    def _load_best_sellers(self):
        for widget in self.best_frame.winfo_children():
            widget.destroy()

        try:
            rows = self.db.fetch_all(
                """
                SELECT i.id, i.name, i.price, SUM(s.quantity) AS qty
                FROM sales s
                JOIN items i ON s.items_id = i.id
                GROUP BY i.id, i.name, i.price
                ORDER BY qty DESC
                LIMIT 6
                """
            )
            self._best_seller_ids = {r[0] for r in rows}

            for row in rows:
                product_id, name, price, qty = row
                btn = tk.Button(
                    self.best_frame,
                    text=f"{name}\nRM {float(price):,.2f}",
                    font=("Segoe UI", 10, "bold"),
                    width=14,
                    height=3,
                    command=lambda p=(product_id, name, price): self.add_to_cart(p),
                )
                btn.pack(side="left", padx=6, pady=6)
        except Exception as e:
            print(f"Best sellers load error: {e}")

    # ---------------------------------------------------------
    # Cart
    # ---------------------------------------------------------

    def add_to_cart(self, product):
        product_id = product[0]
        name = product[1]
        price = float(product[2])
        stock = int(product[3]) if len(product) > 3 else 9999

        current_quantity = self.cart.get(product_id, {}).get("quantity", 0)

        if current_quantity >= stock:
            warning(f"{name} only has {stock} available.")
            return

        if product_id in self.cart:
            self.cart[product_id]["quantity"] += 1
        else:
            self.cart[product_id] = {
                "id": product_id,
                "name": name,
                "price": price,
                "quantity": 1,
                "stock_quantity": stock,
            }

        self.refresh_cart()

    def refresh_cart(self):
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)

        subtotal = 0

        for product in self.cart.values():
            item_total = product["price"] * product["quantity"]
            subtotal += item_total

            self.cart_tree.insert(
                "",
                "end",
                values=(
                    product["name"],
                    product["quantity"],
                    f"RM {item_total:,.2f}",
                ),
            )

        discount = 0
        tax = 0
        total = subtotal - discount + tax

        self.subtotal_label.config(text=f"RM {subtotal:,.2f}")
        self.discount_label.config(text=f"RM {discount:,.2f}")
        self.tax_label.config(text=f"RM {tax:,.2f}")
        self.total_label.config(text=f"RM {total:,.2f}")

    def remove_selected(self):
        selected = self.cart_tree.selection()
        if not selected:
            return

        index = self.cart_tree.index(selected[0])
        item_id = list(self.cart.keys())[index]
        del self.cart[item_id]
        self.refresh_cart()

    def clear_cart(self):
        self.cart.clear()
        self.refresh_cart()

    # ---------------------------------------------------------
    # Checkout
    # ---------------------------------------------------------

    def checkout(self):
        if not self.cart:
            warning("Please add a product first.")
            return

        for product in self.cart.values():
            if product["quantity"] <= 0:
                warning("Quantity must be greater than zero.")
                return

            available = product.get("stock_quantity", 0)
            if product["quantity"] > available:
                warning(f"{product['name']} has only {available} available.")
                return

        total = sum(product["price"] * product["quantity"] for product in self.cart.values())
        payment_method = self.payment_method.get()

        confirm = messagebox.askyesno(
            "Confirm Sale",
            f"Total: RM {total:,.2f}\nPayment: {payment_method}\n\nComplete this sale?",
        )

        if not confirm:
            return

        user = self.controller.current_user
        if not user:
            error("Please log in again.")
            return

        try:
            result = self.sales_service.checkout(
                list(self.cart.values()),
                user["id"],
                payment_method,
            )

            success(f"Sale #{result['sale_id']} completed successfully.")

            self.cart.clear()
            self.refresh_cart()
            self.after(0, self._do_load_products)

        except ValueError as e:
            warning(str(e))
        except Exception:
            print(f"Database error: {e}")
            error("Something went wrong. Please try again.")
