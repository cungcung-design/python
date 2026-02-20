import tkinter as tk

class DashboardFrame(tk.Frame):
 def __init__(self, parent, controller):
  tk.Frame.__init__(self, parent)
  self.controller = controller

def open_dashboard():
    dashboard = tk.Tk()
    dashboard.title("POS Dashboard")
    dashboard.geometry("800x600")
    dashboard.configure(bg="white")

    frame = tk.Frame(dashboard, bg="white", padx=20, pady=20)
    frame.pack(expand=True)

    tk.Label(
        frame, text="POS SYSTEM DASHBOARD", font=("Arial", 16, "bold"), bg="white"
    ).grid(row=0, column=0, columnspan=2, pady=20)

    tk.Button(
        frame,
        text="POS Sales",
        bg="green",
        fg="white",
        width=30,
        height=2,
        command=lambda:self.controller.show_frame("posSales"),
    ).grid(row=1, column=0, columnspan=2, pady=10)

    tk.Label(frame, text="Management", font=("Arial", 12, "bold"), bg="white").grid(
        row=2, column=0, columnspan=2, pady=10
    )

    tk.Button(
        frame,
        text="Category CRUD",
        width=15,
        height=2,
        command=lambda:self.controller.show_frame("categoryManagement"),
    ).grid(row=3, column=0, padx=10, pady=10)

    tk.Button(
        frame, text="Item CRUD", width=15, height=2, command=lambda:self.controller.show_frame("itemManagement")
    ).grid(row=3, column=1, padx=10, pady=10)

    tk.Button(
        frame, text="Staff CRUD", width=15, height=2, command=lambda: self.controller.show_frame("staffManagement")
    ).grid(row=4, column=0, padx=10, pady=10)

    tk.Button(
        frame, text="Safe List", width=15, height=2, command=lambda: print("Go Safe")
    ).grid(row=4, column=1, padx=10, pady=10)

    tk.Button(
        frame,
        text="Logout",
        bg="red",
        fg="white",
        width=30,
        height=2,
        command=dashboard.destroy,
    ).grid(row=5, column=0, columnspan=2, pady=15)

    dashboard.mainloop()
