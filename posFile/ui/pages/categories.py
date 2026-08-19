import tkinter as tk
from tkinter import ttk, messagebox

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


class CategoryFrame(tk.Frame):
    def __init__(self, parent, controller, db):
        super().__init__(parent, bg=BG_MAIN)

        self.controller = controller
        self.db = db

        # Header
        header = tk.Frame(self, bg=BG_CARD, height=65)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="Category Management",
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
            text="Search category...",
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
            text="+ Add Category",
            command=self.category_form,
            bg=PRIMARY,
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=7,
        ).pack(side="right", padx=5)

        tk.Button(
            toolbar,
            text="Edit",
            command=self.edit_category,
            bg="#F59E0B",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=7,
        ).pack(side="right", padx=5)

        tk.Button(
            toolbar,
            text="Delete",
            command=self.delete_category,
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
            command=self.load_categories,
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
            columns=("ID", "Category", "Products"),
            show="headings",
            height=25,
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Products", text="Products")

        self.tree.column("ID", width=80, anchor="center")
        self.tree.column("Category", width=300, anchor="w")
        self.tree.column("Products", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

    # --------------------------------------------------
    # SEARCH
    # --------------------------------------------------

    def on_search_change(self, *args):
        self.load_categories()

    # --------------------------------------------------
    # LOAD CATEGORIES
    # --------------------------------------------------

    def load_categories(self):
        if not hasattr(self, "tree"):
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        search = self.search_var.get().strip()

        try:
            if search:
                query = """
                    SELECT
                        c.id,
                        c.name,
                        COUNT(i.id) AS product_count
                    FROM categories c
                    LEFT JOIN items i
                        ON i.category_id = c.id
                    WHERE c.name LIKE %s
                    GROUP BY c.id, c.name
                    ORDER BY c.name ASC
                """
                params = (f"%{search}%",)
            else:
                query = """
                    SELECT
                        c.id,
                        c.name,
                        COUNT(i.id) AS product_count
                    FROM categories c
                    LEFT JOIN items i
                        ON i.category_id = c.id
                    GROUP BY c.id, c.name
                    ORDER BY c.name ASC
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
                        row[2],
                    ),
                )

        except Exception:
            error("Something went wrong. Please try again.")

    def category_form(self, values=None):
        window = tk.Toplevel(self)
        window.title("Add Category" if not values else "Edit Category")
        window.geometry("420x320")
        window.resizable(False, False)
        window.configure(bg=BG_CARD)
        window.transient(self)
        window.grab_set()

        tk.Label(
            window,
            text="Add Category" if not values else "Edit Category",
            bg=BG_CARD,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 16, "bold"),
        ).pack(pady=(25, 20))

        form = tk.Frame(window, bg=BG_CARD)
        form.pack(fill="x", padx=40)

        tk.Label(
            form,
            text="Category Name",
            bg=BG_CARD,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(0, 5))

        name_entry = tk.Entry(form, font=("Segoe UI", 11))
        name_entry.pack(fill="x", ipady=6)

        if values:
            name_entry.insert(0, values[1])

        def save():
            name = name_entry.get().strip()

            if not name:
                warning("Please enter a category name.")
                return

            try:
                if values:
                    query = """
                        UPDATE categories
                        SET name = %s
                        WHERE id = %s
                    """

                    self.db.execute_query(query, (name, values[0]))
                else:
                    query = """
                        INSERT INTO categories (name)
                        VALUES (%s)
                    """

                    self.db.execute_query(query, (name,))

                window.destroy()
                self.load_categories()

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
            text="Save Category",
            command=save,
            bg=PRIMARY,
            fg="white",
            font=("Segoe UI", 11, "bold"),
        ).pack(pady=(0, 25), ipadx=20, ipady=7)

    # --------------------------------------------------
    # ADD / EDIT FORM
    # --------------------------------------------------

    def category_form(self, values=None):
        window = tk.Toplevel(self)
        window.title("Add Category" if not values else "Edit Category")
        window.geometry("420x320")
        window.resizable(False, False)
        window.configure(bg=BG_CARD)
        window.transient(self)
        window.grab_set()

        tk.Label(
            window,
            text="Add Category" if not values else "Edit Category",
            bg=BG_CARD,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 16, "bold"),
        ).pack(pady=(25, 20))

        form = tk.Frame(window, bg=BG_CARD)
        form.pack(fill="x", padx=40)

        tk.Label(
            form,
            text="Category Name",
            bg=BG_CARD,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(0, 5))

        name_entry = tk.Entry(form, font=("Segoe UI", 11))
        name_entry.pack(fill="x", ipady=6)

        if values:
            name_entry.insert(0, values[1])

        def save():
            name = name_entry.get().strip()

            if not name:
                warning("Please enter a category name.")
                return

            try:
                if values:
                    query = """
                        UPDATE categories
                        SET name = %s
                        WHERE id = %s
                    """

                    self.db.execute_query(query, (name, values[0]))
                else:
                    query = """
                        INSERT INTO categories (name)
                        VALUES (%s)
                    """

                    self.db.execute_query(query, (name,))

                window.destroy()
                self.load_categories()

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
            text="Save Category",
            command=save,
            bg=PRIMARY,
            fg="white",
            font=("Segoe UI", 11, "bold"),
        ).pack(pady=(0, 25), ipadx=20, ipady=7)

    # =========================
    # EDIT
    # =========================

    def edit_category(self):
        selected = self.tree.selection()

        if not selected:
            warning("Please select a category first.")
            return

        values = self.tree.item(selected[0], "values")
        self.category_form(values)

    def delete_category(self):
        selected = self.tree.selection()

        if not selected:
            warning("Please select a category first.")
            return

        values = self.tree.item(selected[0], "values")

        category_id = values[0]
        category_name = values[1]
        product_count = int(values[2])

        if product_count > 0:
            warning(
                f"'{category_name}' has "
                f"{product_count} product(s). "
                "Remove or move those products "
                "before deleting this category."
            )
            return

        confirm = messagebox.askyesno(
            "Delete Category",
            f"Delete '{category_name}'?",
        )

        if not confirm:
            return

        try:
            query = """
                DELETE FROM categories
                WHERE id = %s
            """

            self.db.execute_query(query, (category_id,))

            self.load_categories()
            success("Category deleted successfully.")

        except Exception:
            error("Something went wrong. Please try again.")
