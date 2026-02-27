import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class CategoryFrame(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db

        self.configure(bg="white")

        frame = tk.Frame(self, bg="white", padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(
            frame, text="Category Management", font=("Arial", 15, "bold"), bg="white"
        ).grid(row=0, column=0, columnspan=4, pady=20)

        tk.Label(
            frame, text="Category Name:", font=("Arial", 12, "bold"), bg="white"
        ).grid(row=1, column=0, sticky="e", padx=5, pady=10)

        self.category_name_entry = tk.Entry(frame, width=50)
        self.category_name_entry.grid(row=1, column=1, padx=5, pady=10)

        btn_frame = tk.Frame(frame, bg="white")
        btn_frame.grid(row=2, column=0, columnspan=3, pady=15)

        tk.Button(
            btn_frame,
            text="Create",
            bg="green",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
            command=self.create_category,
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text="Update",
            bg="lightblue",
            font=("Arial", 10, "bold"),
            width=12,
            command=self.update_category,
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            btn_frame,
            text="Delete",
            bg="red",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
            command=self.delete_category,
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            btn_frame,
            text="Back to Dashboard",
            bg="grey",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18,
            command=lambda: self.controller.show_frame("Dashboard"),
        ).grid(row=0, column=3, padx=5)

        tree_frame = tk.Frame(frame, bg="white")
        tree_frame.grid(row=3, column=0, columnspan=4, pady=10)

        self.category_tree = ttk.Treeview(
            tree_frame, columns=("ID", "Name"), show="headings", height=15
        )

        self.category_tree.heading("ID", text="ID")
        self.category_tree.heading("Name", text="Name")

        self.category_tree.column("ID", width=100)
        self.category_tree.column("Name", width=300)

        scrollbar = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.category_tree.yview
        )
        self.category_tree.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.category_tree.pack(fill="both", expand=True)

    def load_categories(self):
        # Clear existing items
        for item in self.category_tree.get_children():
            self.category_tree.delete(item)

        try:
            cursor = self.db.connection.cursor()
            cursor.execute("SELECT id, name FROM categories")
            categories = cursor.fetchall()
            for cat in categories:
                self.category_tree.insert("", "end", values=cat)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load categories: {str(e)}")

    def create_category(self):
        name = self.category_name_entry.get()
        if name:
            try:
                self.db.execute_query(
                    "INSERT INTO categories (name) VALUES (%s)", (name,)
                )
                messagebox.showinfo("Success", "Category created successfully!")
                self.category_name_entry.delete(0, tk.END)
                self.load_categories()
            except Exception as e:
                messagebox.showerror("Database Error:", str(e))
        else:
            messagebox.showwarning("Input Error", "Please enter a category name")

    def update_category(self):
        selected = self.category_tree.selection()
        if selected:
            item = self.category_tree.item(selected)
            category_id = item["values"][0]
            new_name = self.category_name_entry.get()
            if new_name:
                try:
                    self.db.execute_query(
                        "UPDATE categories SET name = %s WHERE id = %s",
                        (new_name, category_id),
                    )
                    messagebox.showinfo("Success", "Category updated successfully!")
                    self.load_categories()
                except Exception as e:
                    messagebox.showerror("Database Error:", str(e))
            else:
                messagebox.showwarning("Input Error", "Please enter a category name")
        else:
            messagebox.showwarning(
                "Selection Error", "Please select a category to update"
            )

    def delete_category(self):
        selected = self.category_tree.selection()
        if selected:
            item = self.category_tree.item(selected)
            category_id = item["values"][0]
            try:
                self.db.execute_query(
                    "DELETE FROM categories WHERE id = %s", (category_id,)
                )
                # Reset AUTO_INCREMENT to 1 after deletion
                self.db.execute_query("ALTER TABLE categories AUTO_INCREMENT = 1")
                messagebox.showinfo("Success", "Category deleted successfully!")
                self.load_categories()
            except Exception as e:
                messagebox.showerror("Database Error:", str(e))
        else:
            messagebox.showwarning(
                "Selection Error", "Please select a category to delete"
            )
