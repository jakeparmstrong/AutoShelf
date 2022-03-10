from tkinter import *
from tkinter import ttk
from DCMotor import DCMotor
from Electromagnet import Electromagnet
from HallEffectSensor import HallEffectSensor
#from Photoresistor import Photoresistor
from LinearActuator import LinearActuator
from EnumTypes import Direction
from EnumTypes import Magnet
import time

# Pin defines
DC_MOTOR_ENA = 2
DC_MOTOR_IN1 = 3
DC_MOTOR_IN2 = 4

LIN_ACT_ENA = 14
LIN_ACT_IN3 = 12
LIN_ACT_IN4 = 18
LIN_ACT_SIG = 23

#PHOTORES = 17
HE_SENSOR = 17

ELECTROMAG = 22

# Constants
NUM_SHELVES = 3

def init():
  # initialize some global variables
  # used in UI
  global shelves
  global free_space_count
  global shelf_buttons
  global frm
  # used in elevation
  global current_floor # state variable used during vertical movement
  global magnet_near   # state variable for hall-effect sensor, used during vertical movement
  current_floor = 0
  magnet_near = False # TODO maybe set to true?
  free_space_count = NUM_SHELVES
  shelves = [False for i in range(NUM_SHELVES)] # 3 shelves. F for empty, T for full
  shelf_buttons = []
  global elevator
  elevator = DCMotor(DC_MOTOR_ENA, DC_MOTOR_IN1, DC_MOTOR_IN2)
  # make sure that the elevator doesn't start moving due to some floating pin:
  elevator.brake()
  global lin_act
  lin_act = LinearActuator(LIN_ACT_ENA, LIN_ACT_IN3, LIN_ACT_IN4, LIN_ACT_SIG)
  global electromagnet
  electromagnet = Electromagnet(ELECTROMAG)
  global he_sensor
  he_sensor = HallEffectSensor(HE_SENSOR)

  for i in range(NUM_SHELVES):
    btn = make_active_btn(i)
    #btn = ttk.Button(frm, text="Storage Space " + str(i), style='my.TButton', command=lambda: retrieve_item(i))
    btn.grid(column=0, row=i, sticky="news")
    btn.grid_remove()
    shelf_buttons.append(btn)

def go_to_floor(floor, direction):
  last_he_reading = Magnet(he_sensor.get_pin_value())  # stores the last hall-effect sensor reading during a floor change
  global current_floor

  if direction == Direction.UP:
    elevator.fwd()
  elif direction == Direction.DOWN:
    elevator.bwd()
  else:
    print("ERROR: invalid direction value passed to go_to_floor()!")

  if floor != current_floor:
    time.sleep(2)
    
  #TODO remove debug statements
  print("On floor %s; Final destination is floor %s" % (current_floor, floor))
  
  #spins with motor running, until 
  while current_floor != floor:
    if Magnet(he_sensor.get_pin_value()) == Magnet.NEAR and last_he_reading == Magnet.FAR:
      # got to next floor
      current_floor = (current_floor + 1) if (direction == Direction.UP) else (current_floor - 1)
      last_he_reading = Magnet.NEAR
      # TODO remove debug
      print("Just arrived at floor %s" % (current_floor))
    elif Magnet(he_sensor.get_pin_value()) == Magnet.FAR  and last_he_reading == Magnet.NEAR:
      # got out of zone of last noted magnet
      last_he_reading = Magnet.FAR
      # TODO remove debug
      print("Just got out of zone of last noted magnet")
  elevator.brake()

def extract_box():
  lin_act.extend_fully()
  electromagnet.on()
  lin_act.retract_fully()
  electromagnet.off() # TODO where to put this?

def store_item(floor):
  electromagnet.on() # TODO when to do this?
  go_to_floor(floor, Direction.UP)
  lin_act.extend_fully()
  electromagnet.off()
  lin_act.retract_fully()
  go_to_floor(0, Direction.DOWN)


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
        store_item(idx)
        return True


def retrieve_item(item_spot):
  global free_space_count
  global shelves
  print(shelves)
  print(item_spot)
  # retrieve the item
  go_to_floor(item_spot, Direction.UP)
  extract_box()
  go_to_floor(0, Direction.DOWN)

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
    else: #Nothing is there
      item.grid()
      item.state(["disabled"])


root = Tk()
# TODO uncomment for touchscreen
#root.config(cursor="none")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.attributes("-fullscreen", True)
s = ttk.Style()
s.configure('my.TButton', font=('Helvetica', 48))
frm = ttk.Frame(root, padding=10)
frm.grid_columnconfigure(0, weight=1)
frm.grid_rowconfigure(0, weight=1)
frm.grid_rowconfigure(1, weight=1)
frm.grid_rowconfigure(2, weight=1)
frm.grid(column=0, row=0, sticky="news")
init()


store_button = ttk.Button(frm, text="Store Item", style='my.TButton', command=store_btn_handler)
store_button.grid(column=0, row=0, sticky="news")

retrieve_button = ttk.Button(frm, text="Retrieve Item", style='my.TButton', command=retrieve_btn_handler)
retrieve_button.grid(column=0, row=1, sticky="nesw")
retrieve_button.state(["disabled"])
#ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, row=2, sticky="enws")
root.mainloop()
