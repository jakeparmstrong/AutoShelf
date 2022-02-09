from tkinter import *
from tkinter import ttk

shelves = [False, False, False] # 3 shelves. F for empty, T for full

def store_handler():
  print("Storing Item")
  # storage_spot = find_storage_space()
  # result = store_in(storage_spot)
  # if result == ...

def retrieve_handler():
  print("Retrieving item")

root = Tk()
root.config(cursor="none")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.attributes("-fullscreen", True)
frm = ttk.Frame(root, padding=10)
frm.grid()

store_button = ttk.Button(frm, text="Store Item", command=store_handler)
store_button.grid(column=0, row=0, sticky="news")

retrieve_button = ttk.Button(frm, text="Retrieve Item", command=retrieve_handler)
retrieve_button.grid(column=0, row=1, sticky="nesw")
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, row=2, sticky="enws")
root.mainloop()
