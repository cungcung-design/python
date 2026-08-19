import tkinter as tk
from tkinter import messagebox
import threading
from database.database import Database
from ui.pages.login import LoginFrame
from ui.pages.dashboard import DashboardFrame
from ui.pages.categories import CategoryFrame
from ui.pages.products import ItemFrame
from ui.pages.reports import SalesReportFrame
from ui.pages.staff import StaffFrame
from ui.pages.pos import POSFrame
from ui.pages.inventory import InventoryFrame
from ui.pages.cash_management import CashManagementFrame
from ui.pages.settings import PlaceholderFrame
from ui.pages.audit import AuditLogFrame
from services.report_service import ReportService
from services.audit_service import AuditService
from services.auth_service import AuthService
from services.product_service import ProductService
from services.sales_service import SalesService
from services.cash_service import CashService
from services.inventory_service import InventoryService
from ui.components.toast import manager


APP_NAME = "Smart POS"
APP_VERSION = "1.1.0"


class POSApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry("900x600")
        self.root.configure(bg="white")

        self.current_user = None

        self.db = Database()
        self.db.setup_database()
        self.audit_service = AuditService(self.db)
        self.report_service = ReportService(self.db)
        self.auth_service = AuthService(self.db, self.audit_service)
        self.product_service = ProductService(self.db, self.audit_service)
        self.sales_service = SalesService(self.db, self.audit_service)
        self.cash_service = CashService(self.db, self.audit_service)
        self.inventory_service = InventoryService(self.db, self.audit_service)
        self.frame = {}
        self.create_frames()
        self.show_frame("Login")

        toast_thread = threading.Thread(target=manager.start, daemon=True)
        toast_thread.start()

    def create_frames(self):
        self.frame["Login"] = LoginFrame(self.root, self, self.db, self.auth_service)
        self.frame["Dashboard"] = DashboardFrame(
            self.root,
            self,
            self.report_service,
        )
        self.frame["POS"] = POSFrame(self.root, self, self.db, self.sales_service)
        self.frame["Category"] = CategoryFrame(self.root, self, self.db)
        self.frame["Item"] = ItemFrame(self.root, self, self.db, self.product_service)
        self.frame["Inventory"] = InventoryFrame(self.root, self, self.db, self.inventory_service)
        self.frame["SalesReport"] = SalesReportFrame(self.root, self, self.db)
        self.frame["Staff"] = StaffFrame(self.root, self, self.db)
        self.frame["CashManagement"] = CashManagementFrame(self.root, self, self.db, self.cash_service)
        self.frame["Settings"] = PlaceholderFrame(self.root, self, "Settings")
        self.frame["Audit"] = AuditLogFrame(self.root, self, self.db, self.audit_service)

        for frame in self.frame.values():
            frame.pack(fill="both", expand=True)

    def show_frame(self, frame_name):
        for frame in self.frame.values():
            frame.pack_forget()
        self.frame[frame_name].pack(fill="both", expand=True)

        if frame_name == "Dashboard":
            self.frame[frame_name].refresh_user()
            self.frame[frame_name].refresh_dashboard()

        elif frame_name == "Category":
            self.frame[frame_name].load_categories()

        elif frame_name == "Item":
            self.frame[frame_name].load_items()

        elif frame_name == "Inventory":
            self.frame[frame_name].load_inventory()

        elif frame_name == "Staff":
            self.frame[frame_name].load_staff()

        elif frame_name == "SalesReport":
            self.frame[frame_name].load_reports()

        elif frame_name == "Audit":
            self.frame[frame_name].load_logs()

    def show_about(self):
        messagebox.showinfo(
            f"About {APP_NAME}",
            (
                f"{APP_NAME}\n"
                f"Version {APP_VERSION}\n\n"
                "Point of Sale System\n"
                "© 2026"
            ),
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = POSApp(root)
    root.mainloop()
