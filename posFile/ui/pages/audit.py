import tkinter as tk
from tkinter import ttk, messagebox

from services.audit_service import AuditService
from services.permission_service import PermissionService

from ui.styles.colors import (
    BG_CARD,
    BG_MAIN,
    BORDER,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)


class AuditLogFrame(tk.Frame):
    def __init__(self, parent, controller, db, audit_service=None):
        super().__init__(parent, bg=BG_MAIN)

        self.controller = controller
        self.db = db
        self.audit_service = audit_service or AuditService(db)

        # Header
        header = tk.Frame(self, bg=BG_CARD, height=65)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="Audit Logs",
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

        # Filters
        filter_frame = tk.Frame(content, bg=BG_MAIN)
        filter_frame.pack(fill="x", pady=(0, 15))

        tk.Label(
            filter_frame,
            text="Action:",
            bg=BG_MAIN,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 10),
        ).pack(side="left")

        self.action_var = tk.StringVar(value="All")
        action_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.action_var,
            state="readonly",
            font=("Segoe UI", 10),
            values=[
                "All",
                "LOGIN_SUCCESS",
                "LOGIN_FAILED",
                "LOGOUT",
                "PRODUCT_CREATED",
                "PRODUCT_UPDATED",
                "PRODUCT_DEACTIVATED",
                "PRICE_CHANGED",
                "STOCK_ADJUSTED",
                "TRANSACTION_CREATED",
                "REGISTER_OPENED",
                "REGISTER_CLOSED",
            ],
        )
        action_combo.pack(side="left", padx=(10, 20), ipady=4)

        tk.Button(
            filter_frame,
            text="Filter",
            command=self.load_logs,
            bg=BG_CARD,
            fg=TEXT_PRIMARY,
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=7,
        ).pack(side="left")

        tk.Button(
            filter_frame,
            text="Refresh",
            command=self.load_logs,
            bg=BG_CARD,
            fg=TEXT_PRIMARY,
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=7,
        ).pack(side="left", padx=(5, 0))

        # Table
        table_frame = tk.Frame(content, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1)
        table_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("Time", "User", "Action", "Entity", "Description"),
            show="headings",
            height=25,
        )
        self.tree.heading("Time", text="Time")
        self.tree.heading("User", text="User")
        self.tree.heading("Action", text="Action")
        self.tree.heading("Entity", text="Entity")
        self.tree.heading("Description", text="Description")

        self.tree.column("Time", width=140, anchor="center")
        self.tree.column("User", width=100, anchor="w")
        self.tree.column("Action", width=160, anchor="w")
        self.tree.column("Entity", width=120, anchor="w")
        self.tree.column("Description", width=400, anchor="w")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        self.load_logs()

    def load_logs(self):
        if not hasattr(self, "tree"):
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        user = self.controller.current_user
        if not user or not PermissionService.can(user.get("role", ""), "settings"):
            messagebox.showerror("Access Denied", "Only administrators can access Audit Logs.")
            self.controller.show_frame("Dashboard")
            return

        try:
            action_filter = self.action_var.get()
            query = """
                SELECT
                    audit_logs.created_at,
                    users.username,
                    audit_logs.action,
                    audit_logs.entity_type,
                    audit_logs.description
                FROM audit_logs
                LEFT JOIN users ON audit_logs.user_id = users.id
            """
            params = ()

            if action_filter != "All":
                query += " WHERE audit_logs.action = %s"
                params = (action_filter,)

            query += " ORDER BY audit_logs.created_at DESC LIMIT 200"

            rows = self.db.fetch_all(query, params)

            for row in rows:
                created_at = row[0]
                username = row[1] or "System"
                action = row[2]
                entity_type = row[3] or ""
                description = row[4] or ""

                time_str = created_at.strftime("%Y-%m-%d %H:%M:%S") if hasattr(created_at, "strftime") else str(created_at)

                self.tree.insert(
                    "",
                    "end",
                    values=(time_str, username, action, entity_type, description),
                )

        except Exception:
            error("Something went wrong. Please try again.")
