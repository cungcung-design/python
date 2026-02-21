import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class StaffFrame(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db

        self.configure(bg="white")

        frame = tk.Frame(self, bg="white", padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(
            frame,
            text="Staff Management",
            background="white",
            font=("Arial", 15, "bold"),
            padx=10,
            pady=10,
        ).grid(row=0, column=0, columnspan=3, padx=10, pady=20)

        tk.Label(
            frame,
            text="Staff Name:",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="black",
        ).grid(row=1, column=0, padx=10, pady=10)

        self.name_entry = tk.Entry(frame, width=40)
        self.name_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(
            frame, text="Role:", font=("Arial", 12, "bold"), bg="white", fg="black"
        ).grid(row=2, column=0, padx=10, pady=10)

        self.role_entry = tk.Entry(frame, width=40)
        self.role_entry.grid(row=2, column=1, padx=10, pady=10)

        btn_frame = tk.Frame(frame, bg="white")
        btn_frame.grid(row=3, column=0, columnspan=4, pady=10)

        tk.Button(
            btn_frame,
            text="Create",
            width=12,
            bg="green",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.create_staff,
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text="Update",
            width=12,
            bg="lightblue",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.update_staff,
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            btn_frame,
            text="Delete",
            width=12,
            bg="red",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.delete_staff,
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            btn_frame,
            text="Back to Dashboard",
            width=14,
            bg="grey",
            fg="white",
            font=("Arial", 10, "bold"),
            command=lambda: self.controller.show_frame("Dashboard"),
        ).grid(row=0, column=3, padx=5, ipadx=5)

        # Treeview for staff list
        tree_frame = tk.Frame(frame, bg="white")
        tree_frame.grid(row=4, column=0, columnspan=3, pady=10)

        self.staff_tree = ttk.Treeview(
            tree_frame, columns=("ID", "Name", "Role"), show="headings", height=15
        )

        self.staff_tree.heading("ID", text="ID")
        self.staff_tree.heading("Name", text="Name")
        self.staff_tree.heading("Role", text="Role")

        self.staff_tree.column("ID", width=100)
        self.staff_tree.column("Name", width=200)
        self.staff_tree.column("Role", width=200)

        scrollbar = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.staff_tree.yview
        )
        self.staff_tree.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.staff_tree.pack(fill="both", expand=True)

    def load_staff(self):
        # Clear existing items
        for item in self.staff_tree.get_children():
            self.staff_tree.delete(item)

        try:
            cursor = self.db.connection.cursor()
            cursor.execute("SELECT id, name, role FROM staff")
            staff = cursor.fetchall()
            for s in staff:
                self.staff_tree.insert("", "end", values=s)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load staff: {str(e)}")

    def create_staff(self):
        name = self.name_entry.get()
        role = self.role_entry.get()

        if name and role:
            try:
                self.db.execute_query(
                    "INSERT INTO staff (name, role) VALUES (%s, %s)", (name, role)
                )
                messagebox.showinfo("Success", "Staff created successfully!")
                self.clear_entries()
                self.load_staff()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create staff: {str(e)}")
        else:
            messagebox.showwarning("Input Error", "Please enter staff name and role")

    def update_staff(self):
        selected = self.staff_tree.selection()
        if selected:
            item = self.staff_tree.item(selected)
            staff_id = item["values"][0]
            name = self.name_entry.get()
            role = self.role_entry.get()

            if name and role:
                try:
                    self.db.execute_query(
                        "UPDATE staff SET name = %s, role = %s WHERE id = %s",
                        (name, role, staff_id),
                    )
                    messagebox.showinfo("Success", "Staff updated successfully!")
                    self.clear_entries()
                    self.load_staff()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update staff: {str(e)}")
            else:
                messagebox.showwarning(
                    "Input Error", "Please enter staff name and role"
                )
        else:
            messagebox.showwarning(
                "Selection Error", "Please select a staff member to update"
            )

    def delete_staff(self):
        selected = self.staff_tree.selection()
        if selected:
            item = self.staff_tree.item(selected)
            staff_id = item["values"][0]
            try:
                self.db.execute_query("DELETE FROM staff WHERE id = %s", (staff_id,))
                messagebox.showinfo("Success", "Staff deleted successfully!")
                self.load_staff()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete staff: {str(e)}")
        else:
            messagebox.showwarning(
                "Selection Error", "Please select a staff member to delete"
            )

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.role_entry.delete(0, tk.END)
