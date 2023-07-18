import os, time
import tkinter as tk
from tkinter import ttk
import threading
from shockcart import Shockcart # bringing in the Shockcart class
from datetime import datetime
cart1 = Shockcart(3,10) # instance of shockcart args(cycle_count,cycle_time)

##############################################
#       GUI app that works with shockcart.py class 
#           RUN THIS to map all touchscreen input to hdmi-2
#           < xinput map-to-output 6 "HDMI-2" >
#       have to run this to manually set the touchscreen input for monitor number 2
#       compile with 
#
# oneliner push 
# git add shockcart.py shockcartUI.py;git commit -m 'temp logging';git push
##############################################


#########VARS###########
app = tk.Tk()
app.geometry("1024x600")
temp_data = tk.StringVar()
counter_num = tk.StringVar()
timer_num = tk.StringVar()
run_var = tk.StringVar()
run_flag = tk.BooleanVar() # pre-define a bool that we'll use to set a run flag

# define windows/frame objects
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

# slightly changed run function, instead of run button starting the shockcart run process
# make a function that runs the run_button functtion but also sets a flag so that we can start a timer

def test_start():
    cart1.run_loop_process()
    run_flag.set(True)

run_button = ttk.Button(
    button_frame,
    text=f"\tRUN\n{cart1.cycle_count} Cycles {cart1.cycle_time * 2} Minutes Per Cycle",
    command=test_start,
)
def kill():
    cart1.kill_loop_process() # terminate the run process
    run_flag.set(False) # reset run_flag to False which changes update_timer() function to set the timer back to zero
    
log_button = tk.Button(
    button_frame,
    text=f"Start temp log\n{cart1.set_datetime()}",
    command=cart1.temp_logger_process,
)

stop_log = tk.Button(
    button_frame,
    text="Stop Log",
    command=cart1.kill_temp_logging,
)

kill_button = ttk.Button(
    button_frame,
    text=f"kill",
    command=kill
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

################# STATUS WINDOW ######################

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
    font=("Helvetica", 16, "bold"),
)

counter_label = tk.Label(
    info_frame,
    textvariable=counter_num,
    )

run_label = tk.Label(
    info_frame,
    textvariable=run_var,
)

def update_run_status():
    if run_flag.get():
        run_var.set(f"Test In Progress")
        run_label.config(fg='green')
    else:
        run_var.set("Inactive... Press RUN to begin test")
        run_label.config(fg='red')
    app.after(1000,update_run_status)
    
        
def update_counter():
    new_counter_num = cart1.get_counter()
    counter_num.set(f"Cycle Count\n{new_counter_num}/{cart1.cycle_count}")
    app.after(1000,update_counter)

timer_label = tk.Label(
    info_frame,
    textvariable=timer_num,
    )

def update_timer():
    if run_flag.get(): # if the run flag was set to true
        timer_num.set(f"Timer\n{cart1.test_time()}/{cart1.cycle_time}")
    else: # just put 0 minutes out of cycle_time minutes
        timer_num.set(f"Timer\n0/{cart1.cycle_time}")
    app.after(1000,update_timer)
    
    
################# STATUS WINDOW ######################

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
log_button.pack()
stop_log.pack()

##########STATUS#############
info_frame.pack(side="right",expand="true",fill="both")
status_label.pack()
run_label.pack()
display_temp_label.pack()
update_run_status()
update_temp_data()
counter_label.pack()
timer_label.pack()
update_counter()
update_timer()
##########STATUS#############

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
    

