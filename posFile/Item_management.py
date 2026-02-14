import tkinter as tk

def hello():
    print("hello")

root = tk.Tk()
root.title("POS SYSTEM")
root.geometry("800x700")
root.configure(bg="white")

frame = tk.Frame(root, bg="white", padx=20, pady=20)
frame.grid(row=0, column=0)

root.grid_rowconfigure(0, weight=0)
root.grid_columnconfigure(0, weight=1)


tk.Label( frame, text="Item Management", font=("Arial", 15, "bold"),bg="white"
).grid(row=0, column=0, columnspan=4, pady=20)

tk.Label(frame, text="Item Name:", font=("Arial", 12, "bold"), bg="white")\
    .grid(row=1, column=0, sticky="e", padx=5, pady=10)

tk.Entry(frame, width=30).grid(row=1, column=1, padx=5, pady=10)

tk.Label(frame, text="Price:", font=("Arial", 12, "bold"), bg="white").grid(row=1, column=2, sticky="e", padx=5, pady=10)

tk.Entry(frame, width=30).grid(row=1, column=3, padx=5, pady=10)

tk.Label(frame, text="Barcode:", font=("Arial", 12, "bold"), bg="white").grid(row=2, column=0, sticky="e", padx=5, pady=10)

tk.Entry(frame, width=30).grid(row=2, column=1, padx=5, pady=10)

tk.Label(frame, text="Category:", font=("Arial", 12, "bold"), bg="white").grid(row=2, column=2, sticky="e", padx=5, pady=10)

tk.Entry(frame, width=30).grid(row=2, column=3, padx=5, pady=10)

tk.Button(frame, text="Create", bg="green", fg="white",
          font=("Arial", 10, "bold"), width=12,
          command=hello
).grid(row=3, column=0, padx=2, pady=15)

tk.Button(frame, text="Update", bg="lightblue",
          font=("Arial", 10, "bold"), width=12,
          command=hello
).grid(row=3, column=1, padx=2, pady=15)

tk.Button(frame, text="Delete", bg="red", fg="white",
          font=("Arial", 10, "bold"), width=12,
          command=hello
).grid(row=3, column=2, padx=2, pady=15)

tk.Button(frame, text="Back To Dashboard", bg="grey", fg="white",
          font=("Arial", 10, "bold"), width=18,
          command=hello
).grid(row=3, column=3, padx=2, pady=15)

tk.Label(frame, text="ID", font=("Arial", 10, "bold"), bg="white")\
    .grid(row=4, column=0, padx=10, pady=5, sticky="nsew")

tk.Label(frame, text="Name", font=("Arial", 10, "bold"), bg="white")\
    .grid(row=4, column=1, padx=10, pady=5, sticky="nsew")

tk.Label(frame, text="Price", font=("Arial", 10, "bold"), bg="white")\
    .grid(row=4, column=2, padx=10, pady=5, sticky="nsew")

tk.Label(frame, text="Barcode", font=("Arial", 10, "bold"), bg="white")\
    .grid(row=4, column=3, padx=10, pady=5, sticky="nsew")

tk.Label(frame, text="Category", font=("Arial", 10, "bold"), bg="white")\
    .grid(row=4, column=4, padx=10, pady=5, sticky="nsew")


root.mainloop()
