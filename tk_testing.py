import os
import tkinter as tk
from tkinter import ttk
from shockcart import Shockcart # bringing in the Shockcart class
cart1 = Shockcart(1) # instance of shockcart

##############################################
#       GUI app that works with shockcart.py class 
#           RUN THIS to map all touchscreen input to hdmi-2
#           < xinput map-to-output 6 "HDMI-2" >
#       have to run this to manually set the touchscreen input for monitor number 2
#       compile with 
##############################################
os.system("xinput map-to-output 6 \"HDMI-2\"") 

# root window
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
    text=f"run {cart1.cycle_time} minutes",
    command=lambda: cart1.run()
)

fill_button.pack(
    ipadx=5,
    ipady=5,
    expand=True
)

reset_relay_button.pack()
run_button.pack()


root.mainloop()