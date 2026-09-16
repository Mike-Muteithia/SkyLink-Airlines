from tkinter import *
parent = Tk()
parent.title("Students")
parent.geometry("400x300")
name = Label(parent,text = "Name :")
name.grid(row = 0, column = 0, pady = 10, padx = 5)
e1 = Entry(parent)
e1.grid(row = 0, column = 1)
regno = Label(parent,text = "Regd No :")
regno.grid(row = 1, column = 0, pady = 10, padx = 5)
e2 = Entry(parent)
e2.grid(row = 1, column = 1)
btn = Button(parent,text = "Submit")
btn.grid(row = 3, column = 1)
parent.mainloop()


