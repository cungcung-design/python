import tkinter as tk
from posDashboard import open_dashboard


def login():
    username = entry_username.get()
    password = entry_password.get()

    if username == "admin" and password == "123":
     root.destroy()  
     open_dashboard()

    else:
        msg_label.config(text="Invalid username or password")


root = tk.Tk()
root.title("Login Page")
root.geometry("900x600")
root.configure(bg="lightblue")

frame = tk.Frame(root, bg="white", padx=20, pady=20)
frame.pack(expand=True)

tk.Label(frame, text="POS System Login",
         font=("Arial", 16, "bold"),
         bg="white").grid(row=0, column=0, columnspan=2, pady=20)

tk.Label(frame, text="Username", bg="white")\
    .grid(row=1, column=0, padx=10, pady=10, sticky="e")

entry_username = tk.Entry(frame)
entry_username.grid(row=1, column=1, padx=10, pady=10)

tk.Label(frame, text="Password", bg="white")\
    .grid(row=2, column=0, padx=10, pady=10, sticky="e")

entry_password = tk.Entry(frame, show="*")
entry_password.grid(row=2, column=1, padx=10, pady=10)

tk.Button(frame, text="Login",
          bg="green", fg="white",
          width=20,
          command=login).grid(row=3, column=0, columnspan=2, pady=15)

msg_label = tk.Label(frame, text="", bg="white")
msg_label.grid(row=4, column=0, columnspan=2)

root.mainloop()
