import tkinter as tk
from tkinter import ttk, messagebox

from services.inventory_service import InventoryService

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


class InventoryFrame(tk.Frame):
    def __init__(self, parent, controller, db, inventory_service=None):
        super().__init__(parent, bg=BG_MAIN)

        self.controller = controller
        self.db = db
        self.inventory_service = inventory_service or InventoryService(db)

        # Header
        header = tk.Frame(self, bg=BG_CARD, height=65)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="Inventory Management",
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

        # Stats bar
        stats = tk.Frame(content, bg=BG_MAIN)
        stats.pack(fill="x", pady=(0, 15))

        self.products_label = tk.Label(
            stats,
            text="Products: 0",
            bg=BG_MAIN,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 10, "bold"),
        )
        self.products_label.pack(side="left", padx=(0, 20))

        self.low_stock_label = tk.Label(
            stats,
            text="Low Stock: 0",
            bg=BG_MAIN,
            fg="#DC2626",
            font=("Segoe UI", 10, "bold"),
        )
        self.low_stock_label.pack(side="left", padx=(0, 20))

        self.value_label = tk.Label(
            stats,
            text="Inventory Value: RM 0.00",
            bg=BG_MAIN,
            fg=SUCCESS,
            font=("Segoe UI", 10, "bold"),
        )
        self.value_label.pack(side="left")

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
            text="Adjust Stock",
            command=self.adjust_stock_dialog,
            bg="#F59E0B",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=7,
        ).pack(side="right", padx=5)

        tk.Button(
            toolbar,
            text="+ Stock In",
            command=self.stock_in_dialog,
            bg=SUCCESS,
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=7,
        ).pack(side="right", padx=5)

        tk.Button(
            toolbar,
            text="Refresh",
            command=self.load_inventory,
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
            columns=("ID", "Product", "Price", "Barcode", "Category", "Stock"),
            show="headings",
            height=25,
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Product", text="Product")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Barcode", text="Barcode")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Stock", text="Stock")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Product", width=200, anchor="w")
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
        self.load_inventory()

    # --------------------------------------------------
    # LOAD INVENTORY
    # --------------------------------------------------

    def load_inventory(self):
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
                product_id = row[0]
                name = row[1]
                price = row[2]
                barcode = row[3]
                category = row[4] or ""
                stock = row[5]

                if stock <= 0:
                    status = "OUT OF STOCK"
                elif stock <= 5:
                    status = "LOW STOCK"
                else:
                    status = "IN STOCK"

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        product_id,
                        name,
                        f"RM {float(price):.2f}",
                        barcode,
                        category,
                        stock,
                    ),
                    tags=(status,),
                )

            self.tree.tag_configure("OUT OF STOCK", background="#FEE2E2")
            self.tree.tag_configure("LOW STOCK", background="#FEF3C7")
            self.tree.tag_configure("IN STOCK", background="#D1FAE5")

            low_count = sum(1 for r in rows if r[5] <= 5)
            out_count = sum(1 for r in rows if r[5] <= 0)
            self.products_label.config(text=f"Products: {len(rows)}")
            self.low_stock_label.config(text=f"Low Stock: {low_count}")
            self.value_label.config(
                text=f"Inventory Value: RM {self.inventory_service.get_inventory_value():,.2f}"
            )

        except Exception:
            error("Something went wrong. Please try again.")

    # --------------------------------------------------
    # ADD / EDIT FORM
    # --------------------------------------------------

    def product_form(self, values=None):
        window = tk.Toplevel(self)
        window.title("Add Product" if not values else "Edit Product")
        window.geometry("460x540")
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

        field_names = [
            "Product Name",
            "Price",
            "Barcode",
            "Stock",
        ]

        fields = {}

        for field in field_names:
            tk.Label(
                form,
                text=field,
                bg=BG_CARD,
                fg=TEXT_SECONDARY,
                font=("Segoe UI", 10),
            ).pack(anchor="w", pady=(8, 4))

            entry = tk.Entry(form, font=("Segoe UI", 11))
            entry.pack(fill="x", ipady=5)
            fields[field] = entry

        tk.Label(
            window,
            text="Category",
            bg=BG_CARD,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 10),
        ).pack(anchor="w", padx=40, pady=(12, 4))

        category_combo = ttk.Combobox(
            window,
            state="readonly",
            font=("Segoe UI", 11),
        )
        category_combo.pack(fill="x", padx=40, ipady=5)

        category_query = """
            SELECT id, name
            FROM categories
            ORDER BY name
        """

        categories = self.db.fetch_all(category_query)

        category_map = {}
        category_names = []

        for category in categories:
            category_id = category[0]
            category_name = category[1]
            category_map[category_name] = category_id
            category_names.append(category_name)

        category_combo["values"] = category_names

        if values:
            product_query = """
                SELECT name, price, barcode, stock_quantity, category_id
                FROM items
                WHERE id = %s
            """

            product_data = self.db.fetch_all(product_query, (values[0],))

            if product_data:
                product = product_data[0]
                fields["Product Name"].insert(0, product[0])
                fields["Price"].insert(0, product[1])
                fields["Barcode"].insert(0, product[2] or "")
                fields["Stock"].insert(0, product[3])

                current_category_id = product[4]
                for category_name, category_id in category_map.items():
                    if category_id == current_category_id:
                        category_combo.set(category_name)
                        break

        def save():
            name = fields["Product Name"].get().strip()
            price = fields["Price"].get().strip()
            barcode = fields["Barcode"].get().strip()
            stock = fields["Stock"].get().strip()
            selected_category = category_combo.get()
            category_id = category_map.get(selected_category)

            if not name or not price:
                warning("Product Name and Price are required.")
                return

            try:
                price = float(price)
                stock = int(stock or 0)
            except ValueError:
                error("Price and stock must be valid numbers.")
                return

            user = self.controller.current_user
            user_id = user["id"] if user else None

            try:
                if values:
                    query = """
                        UPDATE items
                        SET
                            name = %s,
                            price = %s,
                            barcode = %s,
                            stock_quantity = %s,
                            category_id = %s
                        WHERE id = %s
                    """

                    self.db.execute_query(
                        query,
                        (
                            name,
                            price,
                            barcode,
                            stock,
                            category_id,
                            values[0],
                        ),
                    )
                else:
                    query = """
                        INSERT INTO items
                            (name, price, barcode, stock_quantity, category_id)
                        VALUES
                            (%s, %s, %s, %s, %s)
                    """

                    self.db.execute_query(
                        query,
                        (
                            name,
                            price,
                            barcode,
                            stock,
                            category_id,
                        ),
                    )

                window.destroy()
                self.load_inventory()

            except Exception:
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

            if self.inventory_service and user_id:
                self.inventory_service.delete_product(product_id, user_id=user_id)

            self.load_inventory()
            success("Product deleted successfully.")

        except Exception:
            error("Something went wrong. Please try again.")

    # =========================
    # STOCK IN / ADJUST
    # =========================

    def stock_in_dialog(self):
        selected = self.tree.selection()

        if not selected:
            warning("Please select a product first.")
            return

        values = self.tree.item(selected[0], "values")
        item_id = values[0]
        product_name = values[1]
        current_stock = values[5]

        self._stock_dialog(
            mode="Stock In",
            item_id=item_id,
            product_name=product_name,
            current_stock=current_stock,
        )

    def adjust_stock_dialog(self):
        selected = self.tree.selection()

        if not selected:
            warning("Please select a product first.")
            return

        values = self.tree.item(selected[0], "values")
        item_id = values[0]
        product_name = values[1]
        current_stock = values[5]

        self._stock_dialog(
            mode="Adjustment",
            item_id=item_id,
            product_name=product_name,
            current_stock=current_stock,
        )

    def _stock_dialog(self, mode, item_id, product_name, current_stock):
        window = tk.Toplevel(self)
        window.title(mode)
        window.geometry("420x420")
        window.resizable(False, False)
        window.configure(bg=BG_CARD)
        window.transient(self)
        window.grab_set()

        tk.Label(
            window,
            text=f"{mode}: {product_name}",
            bg=BG_CARD,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 14, "bold"),
        ).pack(pady=(25, 10))

        tk.Label(
            window,
            text=f"Current Stock: {current_stock}",
            bg=BG_CARD,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 10),
        ).pack()

        quantity_entry = tk.Entry(window, font=("Segoe UI", 14), justify="center")
        quantity_entry.pack(padx=40, fill="x", ipady=6, pady=(15, 0))

        note_entry = tk.Entry(window, font=("Segoe UI", 11))
        note_entry.pack(padx=40, fill="x", ipady=6, pady=(15, 0))

        def save():
            try:
                quantity = int(quantity_entry.get())
            except ValueError:
                error("Enter a valid number.")
                return

            user = self.controller.current_user
            staff_id = user.get("staff_id") if user else None
            user_id = user["id"] if user else None

            try:
                if mode == "Stock In":
                    self.inventory_service.add_stock(
                        item_id,
                        quantity,
                        staff_id,
                        note_entry.get(),
                        user_id=user_id,
                    )
                else:
                    self.inventory_service.adjust_stock(
                        item_id,
                        quantity,
                        staff_id,
                        note_entry.get(),
                        user_id=user_id,
                    )

                window.destroy()
                self.load_inventory()

                success("Inventory updated.")

            except Exception:
                error("Something went wrong. Please try again.")

        tk.Button(
            window,
            text="Cancel",
            command=lambda: window.destroy(),
            bg="#E5E7EB",
            fg="black",
            font=("Segoe UI", 11, "bold"),
        ).pack(pady=(0, 10), ipadx=30, ipady=5)

        tk.Button(
            window,
            text="Save",
            command=save,
            bg=PRIMARY,
            fg="white",
            font=("Segoe UI", 11, "bold"),
        ).pack(pady=(0, 25), ipadx=30, ipady=5)
