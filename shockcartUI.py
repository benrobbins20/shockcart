import os, time
import tkinter as tk
from tkinter import ttk
import threading
from shockcart import Shockcart # bringing in the Shockcart class
cart1 = Shockcart(30,30) # instance of shockcart args(cycle_count,cycle_time)
# this is the full test 30 hours! 1 cycle 1 hour

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
counter_num = tk.StringVar()
timer_num = tk.StringVar()
info_frame = tk.Frame(app,bg="light blue",border=5,relief="groove")
button_frame = tk.Frame(app,bg="light green",border=5,relief="groove")
pad_frame = tk.Canvas(app,bg="light pink",border=5,relief="groove")

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

timer_label = tk.Label(
    info_frame,
    textvariable=timer_num,
    )

def update_timer():
    timer_num.set(f"Timer\n{cart1.test_time()}/{cart1.cycle_time}")
    app.after(1000,update_timer)
    
def connect_objects(b1, b2):
    # connect line between button 1 and button 2
    # calculate center point of button
    b1_center = (b1.winfo_x() + b1.winfo_width() / 2, b1.winfo_y() + b1.winfo_height() / 2)
    b2_center = (b2.winfo_x() + b2.winfo_width() / 2, b2.winfo_y() + b2.winfo_height() / 2)
    #print(f"Button 1 coords:{b1_center}\nButton 2 coords:{b2_center}") # shows the coords 
    
    # draw line
    pad_frame.create_line(b1_center, b2_center)    
    
# follow scheme of numbering
    # cold_out = 1
    # cold_bypass = 2
    # cold_in = 3
    # hot_bypass = 4
    # hot_in = 5
    # hot_out = 6
    # pump = 7
    # fan = 8
   
co1 = tk.Button(pad_frame,text="Cold Outlet")
cb2 = tk.Button(pad_frame,text="Cold Bypass")
ci3 = tk.Button(pad_frame,text="Cold In")
hb4 = tk.Button(pad_frame,text="Hot Bypass")
hi5 = tk.Button(pad_frame,text="Hot In")
ho6 = tk.Button(pad_frame,text="Hot Out")
# not in the flow (ish) diagram layout, will be set aside in the frame
pump_7 = tk.Button(pad_frame,text="Pump")
fan_8 = tk.Button(pad_frame,text="Fan")

junc_to_mut = tk.Label(pad_frame,text="TEE")
junc_from_mut = tk.Label(pad_frame, text="TEE")
mut_outlet = tk.Label(pad_frame, text="MUT Outlet")
mut_inlet = tk.Label(pad_frame, text="MUT Inlet")

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
cart1.create_timer()
timer_label.pack()
update_counter()
update_timer()

###############PACK###################

####PAD#GRID##########

# approx layout
# see how good I can do with grid
# changed Frame to Canvas, can maybe add lines to show flow layout
#####################################################################
#                HO                                                 #
#                                                                   #
#         HB                                                        #
#                                                                   #
#                        HI                                         #
#                                          CI                       #
#                                                                   #
#                                                      CB           #
#                                                                   #    
#  res                               CO                             #
#####################################################################
####PAD#GRID##########
#test_button.pack()
co1.grid(row=9,column=14,pady=10)
cb2.grid(row=8,column=18, padx=5, pady=10)
ci3.grid(row=7, column=16, padx=10, pady=10)
hb4.grid(row=2,column=4,padx=5)
hi5.grid(row=5,column=7)
ho6.grid(row=1,column=6, padx=15,pady=5)
pump_7.grid(column=1, pady=5, padx=5)
fan_8.grid(column=1, pady=5,padx=5)
# junctions
junc_to_mut.grid(row=1,column=16)
junc_from_mut.grid(row=5,column=14)
# ports
mut_outlet.grid(row=1,column=18)
mut_inlet.grid(row=5, column=18)

# have to update the app before trying to get the coords 
app.update()

## test drawing lines
# point to point = center coord to center coord

    
connect_objects(co1,cb2)
connect_objects(cb2,ci3)
connect_objects(hb4,hi5)
connect_objects(ho6,hb4)
connect_objects(co1,junc_from_mut)
connect_objects(ci3,junc_to_mut)
connect_objects(ho6,junc_to_mut)
connect_objects(hi5,junc_from_mut)
connect_objects(junc_from_mut, mut_inlet)
connect_objects(junc_to_mut, mut_outlet)



pad_frame.pack(side="bottom")

try:
    app.title('Shockcart')
    app.mainloop()
except KeyboardInterrupt:
    cart1.relay_plate_reset()
    

