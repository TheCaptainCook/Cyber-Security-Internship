from tkinter import *
from tkinter import ttk

#https://docs.python.org/3/library/tkinter.html#a-hello-world-program


root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text='Hello World!').grid(column=0, row=0)
ttk.Button(frm, text='Quit', command=root.destroy).grid(column=0, row=1)

root.mainloop()