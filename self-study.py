# import tkinter as tk

# root = tk.Tk()
# root.geometry("300x200")

# tk.Label(root, text="Top Label").pack(side="top", pady=5)
# tk.Label(root, text="Bottom Label").pack(side="bottom", pady=5)
# tk.Label(root, text="Left Label").pack(side="left", padx=5)
# tk.Label(root, text="Right Label").pack(side="right", padx=5)

# root.mainloop()

# import tkinter as tk

# root = tk.Tk()
# root.geometry("300x200")

# tk.Label(root, text="Row 0, Col 0").grid(row=0, column=0, padx=5, pady=5)
# tk.Label(root, text="Row 0, Col 1").grid(row=0, column=1, padx=5, pady=5)
# tk.Label(root, text="Row 1, Col 0").grid(row=1, column=0, padx=5, pady=5)
# tk.Label(root, text="Row 1, Col 1").grid(row=1, column=1, padx=5, pady=5)

# root.mainloop()


# import tkinter as tk

# root = tk.Tk()
# root.geometry("300x200")

# tk.Label(root,text="At (50,50)").place(x=50, y=50)
# tk.Label(root,text="At (100,100)").place(x=100, y=100)
# tk.Label(root,text="At (150,150)").place(x=150, y=150)

# root.mainloop()

# import tkinter as tk

# def greet():
#     name = entry.get()
#     label.config(text=f"Hello, {name}!")

# root = tk.Tk()
# root.geometry("350x200")
# root.title("Greeting App with Frames")

# header_frame = tk.Frame(root, bg="lightblue")
# header_frame.pack(fill="both")  # Horizontal full width
# tk.Label(header_frame, text="Welcome!", font=("Arial", 16), bg="lightblue").pack(pady=10)

# # Input Frame
# input_frame = tk.Frame(root)
# input_frame.pack(pady=10)
# entry = tk.Entry(input_frame, width=20)
# entry.pack(side="left", padx=5)
# button = tk.Button(input_frame, text="Greet Me", command=greet)
# button.pack(side="left", padx=5)

# # Output Frame
# output_frame = tk.Frame(root)
# output_frame.pack(pady=10)
# label = tk.Label(output_frame, text="", font=("Arial", 12))
# label.pack()

# root.mainloop()


# import tkinter as tk

# root = tk.Tk()
# root.geometry("300x200")

# img = tk.PhotoImage(file="example.png") 
# tk.Label(root, image=img).pack(pady=10)

# root.mainloop()

# import tkinter as tk

# def open_window():
#     new_win = tk.Toplevel(root)  
#     new_win.title("Second Window")
#     new_win.geometry("250x100")
#     tk.Label(new_win, text="Hello from the second window!").pack(pady=20)

# root = tk.Tk()
# root.geometry("300x150")
# root.title("Main Window")

# tk.Button(root, text="Open New Window", command=open_window).pack(pady=50)

# root.mainloop()

# import tkinter as tk

# def add_item():
#     item = entry.get()
#     if item != "":
#         listbox.insert(tk.END, item)  # listbox ထဲသို့ add
#         entry.delete(0, tk.END)       # entry box clear

# root = tk.Tk()
# root.geometry("300x250")
# root.title("Simple To-Do List")

# # Entry Box
# entry = tk.Entry(root, width=25)
# entry.pack(pady=10)

# # Add Button
# button = tk.Button(root, text="Add Item", command=add_item)
# button.pack(pady=5)

# # Listbox
# listbox = tk.Listbox(root, width=30)
# listbox.pack(pady=10)

# root.mainloop()

# from PyQt5.QtWidgets import QApplication, QLabel, QWidget

# app = QApplication([])
# window = QWidget()
# window.setWindowTitle("PyQt App")
# window.setGeometry(100, 100, 300, 200)
# label = QLabel("Hello PyQt!", window)
# label.move(100, 80)
# window.show()
# app.exec_()


# import math
# a = float(input("enter side A: "))
# b = float(input("enter side B: "))
# c = math.sqrt(pow(a,2) + pow(b,2))
# print(f"The area of the triangle is: ", c = {c})

import tkinter as tk
from tkinter import ttk
import time

def start():
    task = 10
    x = 0
    while x < task:
      time.sleep(1)
      bar["value"]+=10
      x+=1
      percent.set(str(x / task * 100) + "%")
      root.update_idletasks()
root = tk.Tk()

percent = tk.StringVar()
bar = ttk.Progressbar(root, orient="horizontal",length=300, mode="determinate")
bar.pack(padx=10, pady=10)
percetLabel  = tk.Label(root, text="0%" ,textvariable=percent).pack()
button = tk.Button(root, text="Hello",command=start ).pack()


root.mainloop()