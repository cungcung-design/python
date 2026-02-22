import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class ItemFrame(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        self.load_categories_into_combobox()
        self.configure(bg="white")

        frame = tk.Frame(self, bg="white", padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(
            frame, text="Item Management", font=("Arial", 15, "bold"), bg="white"
        ).grid(row=0, column=0, columnspan=4, pady=20)

        tk.Label(frame, text="Item Name:", font=("Arial", 12, "bold"), bg="white").grid(
            row=1, column=0, sticky="e", padx=5, pady=10
        )

        self.name_entry = tk.Entry(frame, width=30)
        self.name_entry.grid(row=1, column=1, padx=5, pady=10)

        tk.Label(frame, text="Price:", font=("Arial", 12, "bold"), bg="white").grid(
            row=1, column=2, sticky="e", padx=5, pady=10
        )

        self.price_entry = tk.Entry(frame, width=30)
        self.price_entry.grid(row=1, column=3, padx=5, pady=10)

        tk.Label(frame, text="Barcode:", font=("Arial", 12, "bold"), bg="white").grid(
            row=2, column=0, sticky="e", padx=5, pady=10
        )

        self.barcode_entry = tk.Entry(frame, width=30)
        self.barcode_entry.grid(row=2, column=1, padx=5, pady=10)

        tk.Label(frame, text="Category:", font=("Arial", 12, "bold"), bg="white").grid(
            row=2, column=2, sticky="e", padx=5, pady=10
        )

        
        self.category_combobox = ttk.Combobox(frame, width=30, state = "readonly")
        self.category_combobox.grid(row=2, column=3, padx=5,pady=10)
        
        self.load_categories_into_combobox()

        tk.Button(
            frame,
            text="Create",
            bg="green",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
            command=self.create_item,
        ).grid(row=3, column=0, padx=2, pady=15)

        tk.Button(
            frame,
            text="Update",
            bg="lightblue",
            font=("Arial", 10, "bold"),
            width=12,
            command=self.update_item,
        ).grid(row=3, column=1, padx=2, pady=15)

        tk.Button(
            frame,
            text="Delete",
            bg="red",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
            command=self.delete_item,
        ).grid(row=3, column=2, padx=2, pady=15)

        tk.Button(
            frame,
            text="Back To Dashboard",
            bg="grey",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18,
            command=lambda: self.controller.show_frame("Dashboard"),
        ).grid(row=3, column=3, padx=2, pady=15)

        # Treeview
        tree_frame = tk.Frame(frame, bg="white")
        tree_frame.grid(row=4, column=0, columnspan=4, pady=10)

        self.item_tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Name", "Price", "Barcode", "Category"),
            show="headings",
            height=15,
        )

        self.item_tree.heading("ID", text="ID")
        self.item_tree.heading("Name", text="Name")
        self.item_tree.heading("Price", text="Price")
        self.item_tree.heading("Barcode", text="Barcode")
        self.item_tree.heading("Category", text="Category")

        self.item_tree.column("ID", width=50)
        self.item_tree.column("Name", width=150)
        self.item_tree.column("Price", width=100)
        self.item_tree.column("Barcode", width=150)
        self.item_tree.column("Category", width=100)

        scrollbar = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.item_tree.yview
        )

        self.item_tree.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.item_tree.pack(fill="both", expand=True)

    def load_items(self):
        # Clear existing items
        for item in self.item_tree.get_children():
            self.item_tree.delete(item)

        try:
            cursor = self.db.connection.cursor()
            cursor.execute("SELECT id, name, price, barcode, category_id FROM items")
            items = cursor.fetchall()
            for item in items:
                self.item_tree.insert("", "end", values=item)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load items: {str(e)}")

    def create_item(self):
        name = self.name_entry.get()
        price = self.price_entry.get()
        barcode = self.barcode_entry.get()
        category = self.category_combobox.get()

        if name and price and category:
            try:
                category_id = self.category_map.get(category)
                self.db.execute_query(
                    "INSERT INTO items (name, price, barcode, category_id) VALUES (%s, %s, %s, %s)",
                    (name, price, barcode, category_id),
                )
                messagebox.showinfo("Success", "Item created successfully!")
                self.clear_entries()
                self.load_items()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create item: {str(e)}")
        else:
            messagebox.showwarning("Input Error", "Please enter item name and price")

    def update_item(self):
        selected = self.item_tree.selection()
        if selected:
            item = self.item_tree.item(selected)
            item_id = item["values"][0]
            name = self.name_entry.get()
            price = self.price_entry.get()
            barcode = self.barcode_entry.get()
            category = self.category_combobox.get()

            if name and price:
                try:
                    self.db.execute_query(
                        "UPDATE items SET name = %s, price = %s, barcode = %s, category_id = %s WHERE id = %s",
                        (name, price, barcode, category, item_id),
                    )
                    messagebox.showinfo("Success", "Item updated successfully!")
                    self.clear_entries()
                    self.load_items()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update item: {str(e)}")
            else:
                messagebox.showwarning(
                    "Input Error", "Please enter item name and price"
                )
        else:
            messagebox.showwarning("Selection Error", "Please select an item to update")

    def delete_item(self):
        selected = self.item_tree.selection()
        if selected:
            item = self.item_tree.item(selected)
            item_id = item["values"][0]
            try:
                self.db.execute_query("DELETE FROM items WHERE id = %s", (item_id,))
                messagebox.showinfo("Success", "Item deleted successfully!")
                self.load_items()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete item: {str(e)}")
        else:
            messagebox.showwarning("Selection Error", "Please select an item to delete")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.barcode_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)


def load_categories_into_combobox(self):
    try:
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT id, name FROM categories")
        rows = cursor.fetchall()
        self.category_map = {name: cat_id for cat_id, name in rows}
        self.category_combobox["values"] = list(self.category_map.keys())
        cursor.close()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load categories: {str(e)}")            