import os
import tkinter as tk
from tkinter import ttk
import threading
from shockcart import Shockcart # bringing in the Shockcart class
cart1 = Shockcart(3,5) # instance of shockcart args(cycle_count,cycle_time)

##############################################
#       GUI app that works with shockcart.py class 
#           RUN THIS to map all touchscreen input to hdmi-2
#           < xinput map-to-output 6 "HDMI-2" >
#       have to run this to manually set the touchscreen input for monitor number 2
#       compile with 
##############################################
os.system("xinput map-to-output 6 \"HDMI-2\"") 

root = tk.Tk()
root.geometry('300x200')
root.resizable(False, False)
root.title('Fill Cart')

fill_button = ttk.Button(
    root,
    text='Fill',
    command=lambda: cart1.fill(True) 
)

reset_relay_button = ttk.Button(
    root,
    text="Reset all relays",
    command=lambda: cart1.relay_plate_reset()
)
run_button = ttk.Button(
    root,
    text=f"run",
    command=lambda: cart1.run_loop_process()
)
kill_button = ttk.Button(
    root,
    text=f"kill",
    command=lambda: cart1.kill_loop_process()
)

cold_loop_button = ttk.Button(
    root,
    text=f"Cold loop on",
    command=lambda: cart1.cold_loop_enable(True)
)
cold_loop_button.pack(
    ipadx=5,
    ipady=5,
    expand=True
)
hot_loop_button = ttk.Button(
    root, 
    text=f"Hot loop on",
    command=lambda: cart1.hot_loop_enable(True)
)
hot_loop_button.pack(
    ipadx=5,
    ipady=5,
    expand=True
)


reset_relay_button.pack()
run_button.pack()
kill_button.pack()
fill_button.pack()

try:
    root.mainloop()
except KeyboardInterrupt:
    cart1.relay_plate_reset()
    

