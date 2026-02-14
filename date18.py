# import tkinter
# print (tkinter.TkVersion)

from tkinter import *
from tkinter import messagebox

root = Tk()
root.title("Python ")
root.geometry("400x400")

# label = Label(root,text="hello ")
# label.pack()

# ayeminsan = Label (root, text = " hello python")
# ayeminsan.pack(padx=80)

# mg = Button(root , text = "clcik me", command= Buttofunc)
# mg.place(x = 50 , y = 50)
# mg.pack(pady=20 , padx=20)


# def helloCallBack():
#    msg=messagebox.showinfo( "Hello Python", "Hello World")
# B = Button(root, text ="Hello", command = helloCallBack)
# B.place(x=50,y=50)

# root.mainloop()


# def show_text():
#     print ("heelo")
#     data = inputData.get()
#     showDataText.config(text = f"{data}")
# inputData = Entry(root)
# btn = Button(root, text="Add the text", command=show_text)

# showDataText = Label(root, text="Your name is : ")

# inputData.pack(pady=20)
# btn.pack(pady=20)
# showDataText.pack(pady=10)


# def helloCallBack():
#    msg=messagebox.showinfo( "Hello Python", "Hello World")
# B = Button(root, text ="Hello", command = helloCallBack)
# B.place(x=50,y=50)


# def showTextBaby():
#     inputdataname = inputdata.get()
#     messagebox.showinfo(    "data",
#         f"{inputdataname}" )
#     label.config(text = f"mawng ba {inputdataname}")

# inputdata = Entry(root)

# label = Label (root, text = "Your name is :")
# button = Button (root, text = " btn ", command= showTextBaby)

# inputdata.pack(pady = 10)
# button.pack(pady= 20)
# label.pack(pady=20)

canva = Canvas(root, width=200, height=200, bg="red")
canva.create_oval(50,120,150,180,fill = "black")
# canva.create_image(50,10,fill= "green")
canva.create_line(10,10,150,150,fill = 'blue')
canva.create_polygon(50,55,60,60, fill = "grey" , )
canva.pack()


root.mainloop()
