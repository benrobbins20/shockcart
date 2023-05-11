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

#########VARS###########
app = tk.Tk()
temp_data = tk.StringVar()
info_frame = tk.Frame(app)

fill_button = ttk.Button(
    app,
    text='Fill',
    command=lambda: cart1.fill(True) 
)

reset_relay_button = ttk.Button(
    app,
    text="Reset all relays",
    command=lambda: cart1.relay_plate_reset()
)

run_button = ttk.Button(
    app,
    text=f"run",
    command=lambda: cart1.run_loop_process()
)

kill_button = ttk.Button(
    app,
    text=f"kill",
    command=lambda: cart1.kill_loop_process()
)

cold_loop_button = ttk.Button(
    app,
    text=f"Cold loop on",
    command=lambda: cart1.cold_loop_enable(True)
)

hot_loop_button = ttk.Button(
    app, 
    text=f"Hot loop on",
    command=lambda: cart1.hot_loop_enable(True)
)

display_temp_label = tk.Label(
    info_frame, 
    textvariable=temp_data,
    relief="ridge",
)

def update_temp_data():
    new_data = cart1.read_temp_test()
    temp_data.set("UUT Temp\n"+str(new_data))
    app.after(1000,update_temp_data)





###############PACK###################
hot_loop_button.pack()
cold_loop_button.pack()
reset_relay_button.pack()
run_button.pack()
kill_button.pack()
fill_button.pack()
display_temp_label.pack(side="top")
update_temp_data()
info_frame.pack(side="bottom")

try:
    app.title('Shockcart')
    app.mainloop()
except KeyboardInterrupt:
    cart1.relay_plate_reset()
    

