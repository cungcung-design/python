import tkinter as tk
from tkinter import ttk

# ================= ROOT =================
root = tk.Tk()
root.title("POS")
root.geometry("900x800")
root.configure(bg="white")

# ================= ROOT GRID =================
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# ================= MAIN FRAME =================
frame = tk.Frame(root, bg="white")
frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

# Configure grid: 1 row, 2 columns
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=3)  # Left = Items
frame.grid_columnconfigure(1, weight=2)  # Right = Cart

# ================= LEFT FRAME (ITEMS) =================
left_frame = tk.Frame(frame, bg="white")
left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

tk.Label(left_frame, text="POS SALES",
         font=("Arial", 15, "bold"), bg="white").pack(pady=10)

tk.Label(left_frame, text="Barcode Search:",
         font=("Arial",12,"bold"), bg="white").pack(anchor="w", pady=5)

search_frame = tk.Frame(left_frame, bg="white")
search_frame.pack(anchor="w", pady=5)

name_entry = tk.Entry(search_frame, width=30)
name_entry.pack(side="left")

tk.Button(search_frame, text="Search", bg="green", fg="white").pack(side="left", padx=5)

tk.Label(left_frame, text="Item:",
         font=("Arial",10,"bold"), bg="white").pack(anchor="w", pady=5)

# -------- Item Table --------
columns = ("ID", "Name", "Price", "Barcode")
item_tree = ttk.Treeview(left_frame, columns=columns, show="headings", height=15)
item_tree.pack(fill="both", expand=True)

for col in columns:
    item_tree.heading(col, text=col)
    item_tree.column(col, width=120, anchor="center")

# Sample Items
sample_items = [
    (1, "Apple", 1.5, "111"),
    (2, "Orange", 2.0, "222"),
    (3, "Banana", 1.2, "333"),
]

for item in sample_items:
    item_tree.insert("", "end", values=item)

# ================= RIGHT FRAME (CART) =================
right_frame = tk.Frame(frame, bg="white")
right_frame.grid(row=0, column=1, sticky="nsew", pady=(20,0))  # top margin 20px

tk.Label(right_frame, text="Cart:",
         font=("Arial",10,"bold"), bg="white").pack(anchor="w", pady=5)

cart_columns = ("Name", "Price", "Qty", "Total")
cart_tree = ttk.Treeview(right_frame, columns=cart_columns, show="headings", height=15)
cart_tree.pack(fill="both", expand=True)

for col in cart_columns:
    cart_tree.heading(col, text=col)
    cart_tree.column(col, width=90, anchor="center")

# -------- Cart Buttons --------
button_frame = tk.Frame(right_frame, bg="white")
button_frame.pack(pady=5, anchor="w")

tk.Button(button_frame, text="+", width=5).pack(side="left", padx=2)
tk.Button(button_frame, text="-", width=5).pack(side="left", padx=2)
tk.Button(button_frame, text="Remove", width=10).pack(side="left", padx=2)
tk.Button(button_frame, text="Clear Cart", width=10).pack(side="left", padx=2)

# -------- Total --------
total_frame = tk.Frame(right_frame, bg="white")
total_frame.pack(fill="x", pady=10)

tk.Label(total_frame, text="Total:", font=("Arial",10,"bold"), bg="white").pack(side="left")
tk.Label(total_frame, text="$0.00", font=("Arial",10,"bold"), bg="white").pack(side="left", padx=5)

# -------- Staff --------
tk.Label(right_frame, text="Staff:", font=("Arial",10,"bold"), bg="white").pack(anchor="w")
tk.Entry(right_frame, width=30).pack(anchor="w", pady=5)

# -------- Checkout --------
checkout_frame = tk.Frame(right_frame, bg="white")
checkout_frame.pack(pady=5, anchor="w")

tk.Button(checkout_frame, text="Check out", bg="green", fg="white", width=18).pack(side="left", padx=5)
tk.Button(checkout_frame, text="Print Receipt", bg="lightblue", fg="white", width=18).pack(side="left", padx=5)

tk.Button(right_frame, text="Back To Dashboard", bg="grey", fg="white", width=18).pack(pady=5, anchor="e")

root.mainloop()
