import tkinter as tk
from tkinter import ttk, messagebox

from utils.validators import positive_number, positive_integer, required

from models.product import Product
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


class ItemFrame(tk.Frame):
    def __init__(self, parent, controller, db, product_service=None):
        super().__init__(parent, bg=BG_MAIN)

        self.controller = controller
        self.db = db
        self.product_service = product_service
        self.category_map = {}

        # Header
        header = tk.Frame(self, bg=BG_CARD, height=65)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="Products",
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

        # Toolbar
        toolbar = tk.Frame(content, bg=BG_MAIN)
        toolbar.pack(fill="x", pady=(0, 15))

        tk.Label(
            toolbar,
            text="Search products...",
            bg=BG_MAIN,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 10),
        ).pack(side="left")

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search_change)

        search_entry = tk.Entry(
            toolbar,
            textvariable=self.search_var,
            font=("Segoe UI", 10),
            width=30,
        )
        search_entry.pack(side="left", padx=(10, 0), ipady=4)

        tk.Button(
            toolbar,
            text="+ Add Product",
            command=self.product_form,
            bg=PRIMARY,
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=7,
        ).pack(side="right", padx=5)

        tk.Button(
            toolbar,
            text="Edit Product",
            command=self.edit_product,
            bg="#F59E0B",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=7,
        ).pack(side="right", padx=5)

        tk.Button(
            toolbar,
            text="Delete Product",
            command=self.delete_product,
            bg="#EF4444",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=7,
        ).pack(side="right", padx=5)

        tk.Button(
            toolbar,
            text="Refresh",
            command=self.load_items,
            bg=BG_CARD,
            fg=TEXT_PRIMARY,
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=7,
        ).pack(side="right", padx=5)

        # Table
        table_frame = tk.Frame(content, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1)
        table_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Name", "Price", "Barcode", "Category", "Stock"),
            show="headings",
            height=25,
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Product")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Barcode", text="Barcode")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Stock", text="Stock")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Name", width=200, anchor="w")
        self.tree.column("Price", width=100, anchor="e")
        self.tree.column("Barcode", width=120, anchor="center")
        self.tree.column("Category", width=120, anchor="w")
        self.tree.column("Stock", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

    # --------------------------------------------------
    # SEARCH
    # --------------------------------------------------

    def on_search_change(self, *args):
        self.load_items()

    # --------------------------------------------------
    # LOAD
    # --------------------------------------------------

    def load_items(self):
        if not hasattr(self, "tree"):
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        search = self.search_var.get().strip()

        try:
            if search:
                query = """
                    SELECT
                        items.id,
                        items.name,
                        items.price,
                        items.barcode,
                        categories.name,
                        items.stock_quantity
                    FROM items
                    LEFT JOIN categories
                        ON items.category_id = categories.id
                    WHERE items.name LIKE %s
                       OR items.barcode LIKE %s
                    ORDER BY items.id DESC
                """
                params = (f"%{search}%", f"%{search}%")
            else:
                query = """
                    SELECT
                        items.id,
                        items.name,
                        items.price,
                        items.barcode,
                        categories.name,
                        items.stock_quantity
                    FROM items
                    LEFT JOIN categories
                        ON items.category_id = categories.id
                    ORDER BY items.id DESC
                """
                params = ()

            rows = self.db.fetch_all(query, params)

            for row in rows:
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        row[0],
                        row[1],
                        f"RM {float(row[2]):.2f}",
                        row[3],
                        row[4] or "",
                        row[5],
                    ),
                )

        except Exception:
            error("Something went wrong. Please try again.")

    # --------------------------------------------------
    # FORM
    # --------------------------------------------------

    def product_form(self, values=None):
        window = tk.Toplevel(self)
        window.title("Add Product" if not values else "Edit Product")
        window.geometry("460x520")
        window.resizable(False, False)
        window.configure(bg=BG_CARD)
        window.transient(self)
        window.grab_set()

        tk.Label(
            window,
            text="Add Product" if not values else "Edit Product",
            bg=BG_CARD,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 16, "bold"),
        ).pack(pady=(25, 20))

        form = tk.Frame(window, bg=BG_CARD)
        form.pack(fill="x", padx=40)

        tk.Label(
            form,
            text="Product Name",
            bg=BG_CARD,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(10, 5))

        name_entry = tk.Entry(form, font=("Segoe UI", 11))
        name_entry.pack(fill="x", ipady=6)

        tk.Label(
            form,
            text="Price",
            bg=BG_CARD,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(15, 5))

        price_entry = tk.Entry(form, font=("Segoe UI", 11))
        price_entry.pack(fill="x", ipady=6)

        tk.Label(
            form,
            text="Barcode",
            bg=BG_CARD,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(15, 5))

        barcode_entry = tk.Entry(form, font=("Segoe UI", 11))
        barcode_entry.pack(fill="x", ipady=6)

        tk.Label(
            form,
            text="Category",
            bg=BG_CARD,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(15, 5))

        category_combo = ttk.Combobox(
            form,
            state="readonly",
            font=("Segoe UI", 11),
        )
        category_combo.pack(fill="x", ipady=6)

        tk.Label(
            form,
            text="Stock",
            bg=BG_CARD,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(15, 5))

        stock_entry = tk.Entry(form, font=("Segoe UI", 11))
        stock_entry.pack(fill="x", ipady=6)

        try:
            categories = self.db.fetch_all("SELECT id, name FROM categories ORDER BY name")
            self.category_map = {name: cat_id for cat_id, name in categories}
            category_combo["values"] = list(self.category_map.keys())
        except Exception:
            error("Something went wrong. Please try again.")

        if values:
            try:
                product_query = """
                    SELECT name, price, barcode, category_id, stock_quantity
                    FROM items
                    WHERE id = %s
                """
                product_data = self.db.fetch_all(product_query, (values[0],))
                if product_data:
                    product = product_data[0]
                    name_entry.insert(0, product[0])
                    price_entry.insert(0, product[1])
                    barcode_entry.insert(0, product[2] or "")
                    stock_entry.insert(0, product[4])
                    current_category_id = product[3]
                    for category_name, category_id in self.category_map.items():
                        if category_id == current_category_id:
                            category_combo.set(category_name)
                            break
            except Exception:
                pass

        def save():
            name = name_entry.get().strip()
            price = price_entry.get().strip()
            barcode = barcode_entry.get().strip()
            category = category_combo.get()
            stock = stock_entry.get().strip()

            error = required(name, "Product name")
            if error:
                error(error)
                return

            error = required(price, "Price")
            if error:
                error(error)
                return

            error = positive_number(price, "Price")
            if error:
                error(error)
                return

            error = required(stock, "Stock")
            if error:
                error(error)
                return

            error = positive_integer(stock, "Stock")
            if error:
                error(error)
                return

            if not category:
                warning("Product Name, Price, and Category are required.")
                return

            category_id = self.category_map.get(category)
            user = self.controller.current_user
            user_id = user["id"] if user else None

            try:
                if values:
                    query = """
                        UPDATE items
                        SET name = %s, price = %s, barcode = %s, category_id = %s, stock_quantity = %s
                        WHERE id = %s
                    """
                    self.db.execute_query(
                        query,
                        (name, price, barcode, category_id, int(stock), values[0]),
                    )
                    if self.product_service and user_id:
                        old_product = self.product_service.get_product_by_id(values[0])
                        new_product = Product(
                            id=values[0],
                            name=name,
                            price=float(price),
                            barcode=barcode,
                            category_id=category_id,
                            stock_quantity=int(stock),
                        )
                        self.product_service.update_product(new_product, user_id=user_id, old_product=old_product)
                else:
                    query = """
                        INSERT INTO items (name, price, barcode, category_id, stock_quantity)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    self.db.execute_query(
                        query,
                        (name, price, barcode, category_id, int(stock)),
                    )
                    if self.product_service and user_id:
                        new_product = Product(
                            id=None,
                            name=name,
                            price=float(price),
                            barcode=barcode,
                            category_id=category_id,
                            stock_quantity=int(stock),
                        )
                        self.product_service.create_product(new_product, user_id=user_id)

                window.destroy()
                self.load_items()

            except Exception:
                print(f"Database error: {e}")
                error("Something went wrong. Please try again.")

        tk.Button(
            window,
            text="Cancel",
            command=lambda: window.destroy(),
            bg="#E5E7EB",
            fg="black",
            font=("Segoe UI", 11, "bold"),
        ).pack(pady=(0, 10), ipadx=20, ipady=5)

        tk.Button(
            window,
            text="Save Product",
            command=save,
            bg=PRIMARY,
            fg="white",
            font=("Segoe UI", 11, "bold"),
        ).pack(pady=(0, 25), ipadx=20, ipady=8)

    # =========================
    # EDIT
    # =========================

    def edit_product(self):
        selected = self.tree.selection()

        if not selected:
            warning("Please select a product first.")
            return

        values = self.tree.item(selected[0], "values")
        self.product_form(values)

    def delete_product(self):
        selected = self.tree.selection()

        if not selected:
            warning("Please select a product first.")
            return

        values = self.tree.item(selected[0], "values")

        product_id = values[0]
        product_name = values[1]

        confirm = messagebox.askyesno(
            "Delete Product",
            f"Delete '{product_name}'?",
        )

        if not confirm:
            return

        user = self.controller.current_user
        user_id = user["id"] if user else None

        try:
            query = """
                DELETE FROM items
                WHERE id = %s
            """

            self.db.execute_query(query, (product_id,))

            if self.product_service and user_id:
                self.product_service.delete_product(product_id, user_id=user_id)

            self.load_items()
            success("Product deleted successfully.")

        except Exception:
            error("Something went wrong. Please try again.")
