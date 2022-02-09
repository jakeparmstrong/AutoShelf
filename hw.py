from tkinter import *
from tkinter import ttk

NUM_SHELVES = 3

def init():
  #initialize some global variables
  global shelves
  global free_space_count
  global shelf_buttons
  global frm
  free_space_count = NUM_SHELVES
  shelves = [False for i in range(NUM_SHELVES)] # 3 shelves. F for empty, T for full
  shelf_buttons = []
  for i in range(NUM_SHELVES):
    btn = make_active_btn(i)
    #btn = ttk.Button(frm, text="Storage Space " + str(i), style='my.TButton', command=lambda: retrieve_item(i))
    btn.grid(column=0, row=i, sticky="news")
    btn.grid_remove()
    shelf_buttons.append(btn)

def store_btn_handler():
  global shelves
  global free_space_count
  print("Storing Item")
  if free_space_count == NUM_SHELVES:
    retrieve_button.state(["!disabled"])
  if free_space_count == 0:
    return False
  else:
    for idx,item in enumerate(shelves):
      if item == False:
        #if store_in(spot):
        shelves[idx] = True
        free_space_count -= 1
        if free_space_count == 0:
          store_button.state(["disabled"])
        return True

def retrieve_item(item_spot):
  global free_space_count
  global shelves
  print(shelves)
  #if retrieve_from(item_spot): //if returns true
  print(item_spot)
  shelves[item_spot] = False
  free_space_count += 1
  print(shelves)

  for item in shelf_buttons:
    item.grid_remove()
  store_button.grid()
  if free_space_count == NUM_SHELVES:
    retrieve_button.state(["disabled"])
  if free_space_count == 1:
    store_button.state(["!disabled"])
  retrieve_button.grid()
  

def make_active_btn(idx):
  b = ttk.Button(frm, text="Storage Space " + str(idx), style='my.TButton', command=lambda: retrieve_item(idx))
  b.grid(column=0, row=idx, sticky="news")
  return b

def retrieve_btn_handler():
  print("Retrieving item")
  global store_button
  global retrieve_button
  
  #hide buttons temporarily
  store_button.grid_remove()
  retrieve_button.grid_remove()
  for idx,item in enumerate(shelf_buttons):
    if shelves[idx] == True: #Something is there
      item.state(["!disabled"])  
      item.grid()
      #make_active_btn(item)
    else: #Nothing is there
      #b = ttk.Button(frm, text="Storage Space " + str(item))
      #b.grid(column=0, row=item, sticky="news")
      item.grid()
      item.state(["disabled"])  
  #hide buttons, new buttons


root = Tk()
# TODO uncomment for touchscreen
#root.config(cursor="none")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.attributes("-fullscreen", True)
s = ttk.Style()
s.configure('my.TButton', font=('Helvetica', 24))
frm = ttk.Frame(root, padding=10)
frm.grid(column=0, row=NUM_SHELVES, sticky="news")
init()


store_button = ttk.Button(frm, text="Store Item", style='my.TButton', command=store_btn_handler)
store_button.grid(column=0, row=0, sticky="news")

retrieve_button = ttk.Button(frm, text="Retrieve Item", style='my.TButton', command=retrieve_btn_handler)
retrieve_button.grid(column=0, row=1, sticky="nesw")
retrieve_button.state(["disabled"])
#ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, row=2, sticky="enws")
root.mainloop()
