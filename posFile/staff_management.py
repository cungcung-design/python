import tkinter as  tk

def hello():
    print("hello")

root = tk.Tk()
root.title("pos")
root.geometry("800x700")
root.configure(bg="white")


root.grid_rowconfigure(0, weight=0)
root.grid_columnconfigure(0, weight=1)

frame = tk.Frame(root, bg= "white" , padx=20,pady=20)
frame.grid(row=0,column=0)

tk.Label (frame, text="Staff Management",background="white",font=("Arial",15 ,"bold" ) ,padx=10,pady=10).grid(row=0, column=0, columnspan=3 , padx=10 , pady=20)

tk.Label (frame , text="Staff Name:",font=("Arial",12 ,"bold" ), bg="white", fg="black" ).grid(row=1, column=0 , padx=10, pady=10)

name_entry = tk.Entry(frame ,width=40)
name_entry.grid(row=1,column=1,padx=10,pady=10)


tk.Label (frame , text="Role:",font=("Arial",12 ,"bold" ),bg="white", fg="black"  ).grid(row=2 ,column=0 , padx=10, pady=10)

role_entry = tk.Entry(frame, width=40)
role_entry.grid(row=2, column=1, padx=10, pady=10,)


btn_frame = tk.Frame(frame, bg="white")
btn_frame.grid(row=3, column=0, columnspan=4, pady=10)

tk.Button(btn_frame, text="Create", width=12, bg="green", fg="white",
          font=("Arial", 10, "bold"), command=hello).grid(row=0, column=0, padx=5)

tk.Button(btn_frame, text="Update", width=12, bg="lightblue",fg="white",
          font=("Arial", 10, "bold"), command=hello).grid(row=0, column=1, padx=5)

tk.Button(btn_frame, text="Delete", width=12, bg="red", fg="white",
          font=("Arial", 10, "bold"), command=hello).grid(row=0, column=2, padx=5)

tk.Button(btn_frame, text="Back to Dashboard", width=14, bg="grey", fg="white",
          font=("Arial", 10, "bold"), command=hello).grid(row=0, column=3, padx=5,ipadx=5)


tk.Label(frame, text="Id").grid(row=4, column=0, padx=5, pady=5)
tk.Label(frame, text="Name").grid(row=4, column=1, padx=5, pady=5)
tk.Label(frame, text="Role").grid(row=4, column=3, padx=5, pady=5)

root.mainloop()