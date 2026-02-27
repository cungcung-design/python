import tkinter as tk
from tkinter import ttk
from database import Database
from login import LoginFrame
from posDashboard import DashboardFrame
from categorymangement import CategoryFrame
from Item_management import ItemFrame
from sales_report import SalesReportFrame
from staff_management import StaffFrame
from safe_list_frame import POSSalesFrame
from tkinter import messagebox



class POSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("POS System")
        self.root.geometry("900x600")
        self.root.configure(bg="white")

        self.db = Database()
        self.frame = {}
        self.create_frames()
        self.show_frame("Login")

    def create_frames(self):
        self.frame["Login"] = LoginFrame(self.root, self, self.db)

        self.frame["Dashboard"] = DashboardFrame(self.root, self)
        self.frame["Category"] = CategoryFrame(self.root, self, self.db)
        self.frame["Item"] = ItemFrame(self.root, self, self.db)
        self.frame["SalesReport"] = SalesReportFrame(self.root, self, self.db)
        self.frame["Staff"] = StaffFrame(self.root, self, self.db)
        self.frame["SafeList"] = POSSalesFrame(self.root, self, self.db)

        for frame in self.frame.values():
            frame.pack(fill="both", expand=True)

    def show_frame(self, frame_name):
        for frame in self.frame.values():
            frame.pack_forget()
        self.frame[frame_name].pack(fill="both", expand=True)
        if frame_name == "Category":
            self.frame[frame_name].load_categories()
        elif frame_name == "Item":
            self.frame[frame_name].load_items()
        elif frame_name == "Staff":
            self.frame[frame_name].load_staff()
        elif frame_name == "SalesReport":
            self.frame[frame_name].load_sales_transactions()
        elif frame_name == "SafeList":
            self.frame[frame_name].load_safe_list()


if __name__ == "__main__":
    db = Database()
    db.setup_database()
    root = tk.Tk()
    app = POSApp(root)
    root.mainloop()
