import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class CategoryFrame(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db

def create_category(self):
    name =self.category_name_entry.get()
    if name:
        try:
            self.db.execute_query("INSERT INTO categories (name) VALUES (%s)", (name,))
            messagebox.showinfo("Success", "Category created successfully!")
            self.category_name_entry.delete(0, tk.END)
            self.load_categories()
        except Exception as e:
            messagebox.showerror(f"Database Error:",str(e))
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
                self.db.execute_query("UPDATE categories SET name = %s WHERE id = %s", (new_name, category_id))
                messagebox.showinfo("Success", "Category updated successfully!")
                self.load_categories()
            except Exception as e:
                messagebox.showerror(f"Database Error:",str(e))
        else:
            messagebox.showwarning("Input Error", "Please enter a category name")


def delete_category(self):
    selected = self.category_tree.selection()
    if selected:
        item = self.category_tree.item(selected)
        category_id = item["values"][0]
        try:
            self.db.execute_query("DELETE FROM categories WHERE id = %s", (category_id,))
            messagebox.showinfo("Success", "Category deleted successfully!")
            self.load_categories()
        except Exception as e:
            messagebox.showerror(f"Database Error:",str(e))



root = tk.Tk()
root.title("POS SYSTEM")
root.geometry("800x700")
root.configure(bg="white")

root.grid_rowconfigure(0, weight=0) 
root.grid_columnconfigure(0, weight=1)

frame = tk.Frame(root, bg="white", padx=20, pady=20)
frame.grid(row=0, column=0)

# title
tk.Label(frame, text="Category Management",
         font=("Arial", 15, "bold"),
         bg="white").grid(row=0, column=0, columnspan=4, pady=20)

# input
tk.Label(frame, text="Category Name:",
         font=("Arial", 12, "bold"),
         bg="white").grid(row=1, column=0, sticky="e", padx=5, pady=10)

tk.Entry(frame, width=50).grid(row=1, column=1, padx=5, pady=10)

# buttons
btn_frame = tk.Frame(frame, bg="white")
btn_frame.grid(row=3, column=0, columnspan=3, pady=15)

tk.Button(btn_frame, text="Create", bg="green", fg="white",
          font=("Arial", 10, "bold"), width=12,
          command=create_category).grid(row=0, column=0, padx=5)

tk.Button(btn_frame, text="Update", bg="lightblue",
          font=("Arial", 10, "bold"), width=12,
          command=update_category).grid(row=0, column=1, padx=5)

tk.Button(btn_frame, text="Delete", bg="red", fg="white",
          font=("Arial", 10, "bold"), width=12,
          command=delete_category).grid(row=0, column=2, padx=5)

# Treeview
tree_frame = tk.Frame(frame, bg="white")
tree_frame.grid(row=4, column=0, columnspan=4, pady=10)

category_tree = ttk.Treeview(tree_frame,
                             columns=("ID", "Name"),
                             show="headings",
                             height=15)

category_tree.heading("ID", text="ID")
category_tree.heading("Name", text="Name")

category_tree.column("ID", width=100)
category_tree.column("Name", width=300)

scrollbar = ttk.Scrollbar(tree_frame,
                          orient="vertical",
                          command=category_tree.yview)

category_tree.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
category_tree.pack(fill="both", expand=True)

root.mainloop()
