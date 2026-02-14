import tkinter as tk
from tkinter import ttk
import tkinter.messagebox


class CategoryFrame(tk.Frame):
    def __init__(self, parent, controller=None, db=None):
        super().__init__(parent)
        self.controller = controller
        self.db = db

        self.configure(bg="white", padx=20, pady=20)
        self.grid(row=0, column=0, sticky="")

        # Title
        tk.Label(
            self, text="Category Management", font=("Arial", 15, "bold"), bg="white"
        ).grid(row=0, column=0, columnspan=4, pady=20)

        # Input frame
        tk.Label(
            self, text="Category Name:", font=("Arial", 12, "bold"), bg="white"
        ).grid(row=1, column=0, sticky="e", padx=5, pady=10)

        self.name_entry = tk.Entry(self, width=50)
        self.name_entry.grid(row=1, column=1, padx=5, pady=10)

        # Button frame
        btn_frame = tk.Frame(self, bg="white")
        btn_frame.grid(row=3, column=0, columnspan=3, pady=15)

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

        # TreeView
        tree_frame = tk.Frame(self, bg="white")
        tree_frame.grid(row=4, column=0, columnspan=4, pady=10, sticky="nsew")

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
        self.category_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.category_tree.pack(fill="both", expand=True)

        # Configure grid weights for tree_frame
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

    def create_category(self):
        print("create")

    def update_category(self):
        print("update")

    def delete_category(self):
        print("delete")
    def load_categories(self):
        print("load")


def main():
    root = tk.Tk()
    root.title("POS SYSTEM")
    root.geometry("800x700")
    root.configure(bg="white")

    # Create category frame
    category_frame = CategoryFrame(root)
    category_frame.pack(fill="both", expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()
