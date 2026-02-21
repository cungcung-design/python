import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class SalesReportFrame(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db

        self.configure(bg="white")

        frame = tk.Frame(self, bg="white", padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(
            frame,
            text="Sales Transactions Report",
            font=("Arial", 16, "bold"),
            bg="white",
        ).grid(row=0, column=0, columnspan=3, pady=20)

        tk.Label(
            frame, text="Search by Date:", font=("Arial", 12, "bold"), bg="white"
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.date_entry = tk.Entry(frame, width=15)
        self.date_entry.grid(row=1, column=1, padx=10)

        tk.Button(
            frame,
            text="Search",
            width=12,
            bg="green",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.search_data,
        ).grid(row=1, column=2, padx=5)

        tk.Button(
            frame,
            text="Clear",
            width=12,
            bg="lightblue",
            font=("Arial", 10, "bold"),
            command=self.clear_data,
        ).grid(row=1, column=3, padx=5)

        tree_frame = tk.Frame(frame, bg="white")
        tree_frame.grid(row=2, column=0, columnspan=5, pady=20, sticky="nsew")

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Amount", "Type", "Date", "Staff"),
            show="headings",
        )

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        style.configure(
            "Treeview",
            background="#f0f0f0",
            fieldbackground="#f0f0f0",
            font=(
                "Arial",
                10,
            ),
            rowheight=25,
            foreground="black",
            bordercolor="lightblue",
            borderwidth=2,
            highlightthickness=0,
        )

        for col in ("ID", "Amount", "Type", "Date", "Staff"):
            self.tree.heading(
                col,
                text=col,
            )
            self.tree.column(col, width=100, anchor="center")

        self.tree.grid(row=0, column=0, sticky="nsew", pady=20)

        scrollbar = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        bottom_button_frame = tk.Frame(frame, bg="white")
        bottom_button_frame.grid(row=3, column=0, columnspan=5, pady=10, sticky="ew")

        tk.Button(
            bottom_button_frame,
            text="Refresh",
            width=15,
            bg="orange",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.load_sales_transactions,
        ).pack(side="left", padx=10)

        tk.Button(
            bottom_button_frame,
            text="Print Receipt",
            width=15,
            bg="blue",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.print_receipt,
        ).pack(side="left", padx=10)

        tk.Button(
            bottom_button_frame,
            text="Back to Dashboard",
            width=20,
            bg="grey",
            fg="white",
            font=("Arial", 10, "bold"),
            command=lambda: self.controller.show_frame("Dashboard"),
        ).pack(side="right", padx=10)

    def search_data(self):
        date = self.date_entry.get()
        if date:
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)

            try:
                cursor = self.db.connection.cursor()
                cursor.execute(
                    "SELECT id, amount, type, date, staff_id FROM safe_transactions WHERE DATE(date) = %s",
                    (date,),
                )
                transactions = cursor.fetchall()
                for trans in transactions:
                    self.tree.insert("", "end", values=trans)
            except Exception as e:
                messagebox.showerror("Error", f"Search failed: {str(e)}")
        else:
            messagebox.showwarning("Input Error", "Please enter a date")

    def clear_data(self):
        self.date_entry.delete(0, tk.END)
        self.load_sales_transactions()

    def load_sales_transactions(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            cursor = self.db.connection.cursor()
            cursor.execute(
                "SELECT id, amount, type, date, staff_id FROM safe_transactions"
            )
            transactions = cursor.fetchall()
            for trans in transactions:
                self.tree.insert("", "end", values=trans)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load transactions: {str(e)}")

    def print_receipt(self):
        messagebox.showinfo("Print", "Print functionality not implemented yet")
