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


class StaffFrame(tk.Frame):
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
            text="Staff Management",
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
            text="Search staff...",
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
            text="+ Create User",
            command=self.create_user,
            bg=PRIMARY,
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=7,
        ).pack(side="right", padx=5)

        tk.Button(
            toolbar,
            text="+ Add Staff",
            command=self.staff_form,
            bg=SUCCESS,
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=7,
        ).pack(side="right", padx=5)

        tk.Button(
            toolbar,
            text="Edit",
            command=self.edit_staff,
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
            command=self.delete_staff,
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
            command=self.load_staff,
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
            columns=("ID", "Name", "Role"),
            show="headings",
            height=25,
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Role", text="Role")

        self.tree.column("ID", width=80, anchor="center")
        self.tree.column("Name", width=300, anchor="w")
        self.tree.column("Role", width=200, anchor="w")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

    # --------------------------------------------------
    # SEARCH
    # --------------------------------------------------

    def on_search_change(self, *args):
        self.load_staff()

    # --------------------------------------------------
    # LOAD STAFF
    # --------------------------------------------------

    def load_staff(self):
        if not hasattr(self, "tree"):
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        search = self.search_var.get().strip()

        try:
            if search:
                query = """
                    SELECT id, name, role
                    FROM staff
                    WHERE name LIKE %s
                       OR role LIKE %s
                    ORDER BY id DESC
                """
                params = (f"%{search}%", f"%{search}%")
            else:
                query = """
                    SELECT id, name, role
                    FROM staff
                    ORDER BY id DESC
                """
                params = ()

            rows = self.db.fetch_all(query, params)

            for row in rows:
                self.tree.insert("", "end", values=row)

        except Exception:
            error("Something went wrong. Please try again.")

    def staff_form(self, values=None):
        window = tk.Toplevel(self)
        window.title("Add Staff" if not values else "Edit Staff")
        window.geometry("420x360")
        window.resizable(False, False)
        window.configure(bg=BG_CARD)
        window.transient(self)
        window.grab_set()

        tk.Label(
            window,
            text="Add Staff" if not values else "Edit Staff",
            bg=BG_CARD,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 16, "bold"),
        ).pack(pady=(25, 20))

        form = tk.Frame(window, bg=BG_CARD)
        form.pack(fill="x", padx=40)

        tk.Label(
            form,
            text="Staff Name",
            bg=BG_CARD,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(0, 5))

        name_entry = tk.Entry(form, font=("Segoe UI", 11))
        name_entry.pack(fill="x", ipady=6)

        tk.Label(
            form,
            text="Role",
            bg=BG_CARD,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(15, 5))

        role_entry = tk.Entry(form, font=("Segoe UI", 11))
        role_entry.pack(fill="x", ipady=6)

        if values:
            name_entry.insert(0, values[1])
            role_entry.insert(0, values[2])

        def save():
            name = name_entry.get().strip()
            role = role_entry.get().strip()

            if not name or not role:
                warning("Staff Name and Role are required.")
                return

            try:
                if values:
                    query = """
                        UPDATE staff
                        SET name = %s, role = %s
                        WHERE id = %s
                    """
                    self.db.execute_query(query, (name, role, values[0]))
                else:
                    query = """
                        INSERT INTO staff (name, role)
                        VALUES (%s, %s)
                    """
                    self.db.execute_query(query, (name, role))

                window.destroy()
                self.load_staff()

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
            text="Save Staff",
            command=save,
            bg=PRIMARY,
            fg="white",
            font=("Segoe UI", 11, "bold"),
        ).pack(pady=(0, 25), ipadx=20, ipady=7)

    # =========================
    # EDIT
    # =========================

    def edit_staff(self):
        selected = self.tree.selection()

        if not selected:
            warning("Please select a staff member first.")
            return

        values = self.tree.item(selected[0], "values")
        self.staff_form(values)

    def delete_staff(self):
        selected = self.tree.selection()

        if not selected:
            warning("Please select a staff member.")
            return

        values = self.tree.item(selected[0], "values")

        staff_id = values[0]
        staff_name = values[1]

        confirm = messagebox.askyesno(
            "Delete Staff",
            f"Delete '{staff_name}'?",
        )

        if not confirm:
            return

        try:
            query = """
                DELETE FROM staff
                WHERE id = %s
            """

            self.db.execute_query(query, (staff_id,))

            self.load_staff()
            success("Staff deleted successfully.")

        except Exception:
            error("Something went wrong. Please try again.")

    # =========================
    # CREATE USER ACCOUNT
    # =========================

    def create_user(self):
        window = tk.Toplevel(self)
        window.title("Create User Account")
        window.geometry("420x520")
        window.resizable(False, False)
        window.configure(bg=BG_CARD)
        window.transient(self)
        window.grab_set()

        tk.Label(
            window,
            text="Create User Account",
            bg=BG_CARD,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 16, "bold"),
        ).pack(pady=(25, 20))

        form = tk.Frame(window, bg=BG_CARD)
        form.pack(fill="x", padx=40)

        tk.Label(
            form,
            text="Username",
            bg=BG_CARD,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(0, 5))

        username_entry = tk.Entry(form, font=("Segoe UI", 11))
        username_entry.pack(fill="x", ipady=6)

        tk.Label(
            form,
            text="Password",
            bg=BG_CARD,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(15, 5))

        password_entry = tk.Entry(form, font=("Segoe UI", 11), show="*")
        password_entry.pack(fill="x", ipady=6)

        tk.Label(
            form,
            text="Role",
            bg=BG_CARD,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(15, 5))

        role_combo = ttk.Combobox(
            form,
            state="readonly",
            font=("Segoe UI", 11),
            values=["admin", "manager", "cashier"],
        )
        role_combo.pack(fill="x", ipady=6)
        role_combo.current(2)

        tk.Label(
            form,
            text="Staff Member",
            bg=BG_CARD,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(15, 5))

        staff_combo = ttk.Combobox(
            form,
            state="readonly",
            font=("Segoe UI", 11),
        )
        staff_combo.pack(fill="x", ipady=6, pady=(0, 20))

        try:
            staff_rows = self.db.fetch_all(
                "SELECT id, name FROM staff ORDER BY name"
            )

            staff_map = {}
            staff_labels = []

            for staff_id, name in staff_rows:
                label = f"{staff_id} - {name}"
                staff_map[label] = staff_id
                staff_labels.append(label)

            staff_combo["values"] = staff_labels

            if staff_labels:
                staff_combo.current(0)

        except Exception:
            error("Something went wrong. Please try again.")

        def save_user():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            role = role_combo.get()
            staff_label = staff_combo.get()

            if not username or not password:
                warning("Username and password are required.")
                return

            staff_id = staff_map.get(staff_label)

            try:
                self.db.execute_query(
                    """
                    INSERT INTO users
                        (username, password, role, staff_id)
                    VALUES
                        (%s, %s, %s, %s)
                    """,
                    (
                        username,
                        password,
                        role,
                        staff_id,
                    ),
                )

                success(f"User '{username}' created.")

                window.destroy()

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
            text="Create Account",
            command=save_user,
            bg=SUCCESS,
            fg="white",
            font=("Segoe UI", 11, "bold"),
        ).pack(pady=(0, 25), ipadx=20, ipady=7)
