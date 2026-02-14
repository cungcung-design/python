import tkinter as tk
from tkinter import ttk

def search_data():
    print("Search clicked")

def clear_data():
    
    print("Cleared")

root = tk.Tk()
root.title("POS - Sales Transactions Report")
root.geometry("900x600")
root.configure(bg="white")
root.grid_rowconfigure(0, weight=4)
root.grid_columnconfigure(0, weight=2)

frame = tk.Frame(root, bg="white", padx=20, pady=20)
frame.grid(row=0, column=0, sticky="nsew")

tk.Label( frame, text="Sales Transactions Report", font=("Arial", 16, "bold"), bg="white"
).grid(row=0, column=0, columnspan=3, pady=20)

tk.Label(frame, text="Search by Date:", font=("Arial", 12, "bold"), bg="white")\
    .grid(row=1, column=0, padx=10, pady=10, sticky="w")

date_entry = tk.Entry(frame, width=15)
date_entry.grid(row=1, column=1, padx=10)

tk.Button(
    frame, text="Search", width=12,
    bg="green", fg="white",
    font=("Arial", 10, "bold"),
    command=search_data
).grid(row=1, column=2, padx=5)

tk.Button(
    frame, text="Clear", width=12,
    bg="lightblue",
    font=("Arial", 10, "bold"),
    command=clear_data
).grid(row=1, column=3, padx=5)

tree = ttk.Treeview(
    frame,
    columns=("ID", "Amount", "Type", "Date", "Staff"),
    show="headings"
)

style= ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading",font=("Arial", 12, "bold") )
style.configure("Treeview", background="#f0f0f0", fieldbackground="#f0f0f0", font=("Arial", 10,), rowheight=25, foreground="black", bordercolor="lightblue", borderwidth=2, highlightthickness=0)

for col in ("ID", "Amount", "Type", "Date", "Staff"):
    tree.heading(col, text=col ,)
    tree.column(col, width=100, anchor="center")

tree.grid(row=3, column=0, columnspan=5, sticky="nsew", pady=20)

bottom_button_frame = tk.Frame(frame, bg="white")
bottom_button_frame.grid(row=4, column=0, columnspan=5, pady=10, sticky="ew")

tk.Button(
    bottom_button_frame, text="Refresh", width=15, 
    bg="orange", fg="white", font=("Arial", 10, "bold")
).pack(side="left", padx=10)

tk.Button(
    bottom_button_frame, text="Print Receipt", width=15, 
    bg="blue", fg="white", font=("Arial", 10, "bold")
).pack(side="left", padx=10)

tk.Button(
    bottom_button_frame, text="Back to Dashboard", width=20, 
    bg="grey", fg="white", font=("Arial", 10, "bold")
).pack(side="right", padx=10)
# tree.insert("", "end", values=(1, 15000, "Cash", "2026-01-20", "John"))
# tree.insert("", "end", values=(2, 22000, "Card", "2026-01-21", "Anna"))

root.mainloop()

# import tkinter as tk
# from tkinter import ttk  # For better looking widgets and Treeview
# import mysql.connector

# class SalesReportApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("POS - Sales Transactions Report")
#         self.root.geometry("900x700")
#         self.root.configure(bg="#f0f0f0") # Light gray background for a modern look

#         # Main Container
#         self.main_frame = tk.Frame(self.root, bg="white", padx=20, pady=20)
#         self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

#         self.create_header()
#         self.create_search_bar()
#         self.create_table()

#     def create_header(self):
#         title = tk.Label(
#             self.main_frame, text="Sales Transactions Report",
#             font=("Arial", 18, "bold"), bg="white", fg="#333"
#         )
#         title.pack(pady=(0, 20))

#     def create_search_bar(self):
#         search_frame = tk.Frame(self.main_frame, bg="white")
#         search_frame.pack(fill="x", pady=10)

#         tk.Label(search_frame, text="Search by Date:", font=("Arial", 11), bg="white").pack(side="left", padx=5)
        
#         self.date_entry = tk.Entry(search_frame, font=("Arial", 11))
#         self.date_entry.pack(side="left", padx=5)

#         tk.Button(search_frame, text="Search", bg="#2ecc71", fg="white", 
#                   width=10, command=self.search_data).pack(side="left", padx=5)
        
#         tk.Button(search_frame, text="Clear", bg="#3498db", fg="white", 
#                   width=10, command=self.clear_data).pack(side="left", padx=5)

#     def create_table(self):
#         # Using Treeview for organized columns
#         columns = ("id", "amount", "type", "date", "staff")
#         self.tree = ttk.Treeview(self.main_frame, columns=columns, show="headings")

#         # Define Headings
#         self.tree.heading("id", text="ID")
#         self.tree.heading("amount", text="Amount")
#         self.tree.heading("type", text="Type")
#         self.tree.heading("date", text="Date")
#         self.tree.heading("staff", text="Staff")

#         # Column widths
#         self.tree.column("id", width=50)
#         self.tree.column("amount", width=100)
        
#         self.tree.pack(fill="both", expand=True)

#     def search_data(self):
#         print(f"Searching for: {self.date_entry.get()}")
#         # Add your MySQL logic here

#     def clear_data(self):
#         self.date_entry.delete(0, tk.END)

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = SalesReportApp(root)
#     root.mainloop()