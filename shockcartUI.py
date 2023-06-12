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
#
#  
##############################################


#########VARS###########
app = tk.Tk()
temp_data = tk.StringVar()
counter_num =tk.StringVar()
info_frame = tk.Frame(app,bg="light blue",border=5,relief="groove")
button_frame = tk.Frame(app,bg="light green",border=5,relief="groove")
pad_frame = tk.Frame(app,bg="light pink",border=5,relief="groove")



fill_button = ttk.Button(
    button_frame,
    text='Fill',
    command=lambda: cart1.fill(True) 
)

reset_relay_button = ttk.Button(
    button_frame,
    text="Reset all relays",
    command=lambda: cart1.relay_plate_reset()
)

run_button = ttk.Button(
    button_frame,
    text=f"run",
    command=lambda: cart1.run_loop_process()
)

kill_button = ttk.Button(
    button_frame,
    text=f"kill",
    command=lambda: cart1.kill_loop_process()
)

cold_loop_button = ttk.Button(
    button_frame,
    text=f"Cold loop on",
    command=lambda: cart1.cold_loop_enable(True)
)

hot_loop_button = ttk.Button(
    button_frame, 
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

status_label = tk.Label(
    info_frame,
    text="Status",
)

counter_label = tk.Label(
    info_frame,
    textvariable=counter_num,
    )

def update_counter():
    new_counter_num = cart1.get_counter()
    counter_num.set(f"Cycle Count\n{new_counter_num}/{cart1.cycle_count}")
    app.after(1000,update_counter)

toggle_button = tk.Button(pad_frame,text="test")

###############PACK###################
button_frame.pack(side="left",expand="true",fill="both")
hot_loop_button.pack()
cold_loop_button.pack()
reset_relay_button.pack()
run_button.pack()
kill_button.pack()
fill_button.pack()

info_frame.pack(side="right",expand="true",fill="both")
status_label.pack()
display_temp_label.pack()
update_temp_data()
counter_label.pack()
update_counter()

pad_frame.pack(side="bottom",expand="true",fill="both")
toggle_button.pack()

try:
    app.title('Shockcart')
    app.mainloop()
except KeyboardInterrupt:
    cart1.relay_plate_reset()
    

