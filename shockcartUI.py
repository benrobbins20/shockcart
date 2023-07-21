import os, time
import tkinter as tk
from tkinter import ttk
import threading
from shockcart import Shockcart # bringing in the Shockcart class
from datetime import datetime
cart1 = Shockcart(5,30) # instance of shockcart args(cycle_count,cycle_time)

##############################################
#       GUI app that works with shockcart.py class 
#           RUN THIS to map all touchscreen input to hdmi-2
#           < xinput map-to-output 6 "HDMI-2" >
#       have to run this to manually set the touchscreen input for monitor number 2
#       compile with 
#       pyinstaller --onefile shockcartUI.py ;sudo chmod +x dist/shockcartUI;cp dist/shockcartUI ~/Desktop
#
# oneliner push 
# git add shockcart.py shockcartUI.py;git commit -m 'toggle not working only on relay 3???';git push
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

button_frame = tk.Frame(app,bg="light green",border=5,relief="groove",width=190,height=200)
pad_canvas = tk.Canvas(app,bg="light pink",border=5,relief="groove",width=822,height=388)
info_frame = tk.Frame(app,bg="light blue",border=5,relief="groove",width=190,height=200)
terminal_frame = tk.Frame(app,width=1024,height=180)

##############BUTTONS################

def test_start():
    cart1.run_loop_process()
    #cart1.temp_logger_process()
    run_flag.set(True)

def kill():
    cart1.kill_loop_process() # terminate the run process
    run_flag.set(False) # reset run_flag to False which changes update_timer() function to set the timer back to zero

fill_button = ttk.Button(
    button_frame,
    text='Fill',
    command=lambda: cart1.fill(True) 
)

reset_relay_button = ttk.Button(
    button_frame,
    text="Reset Relays",
    command=lambda: cart1.relay_plate_reset()
)

run_button = ttk.Button(
    button_frame,
    text=f"             RUN\n{cart1.cycle_count} Cycles:{cart1.cycle_time * 2} Minutes",
    command=test_start,
)

log_button = tk.Button(
    button_frame,
    text=f"Start temp log",
    command=cart1.temp_logger_process,
)

stop_log = tk.Button(
    button_frame,
    text="Stop Log",
    command=cart1.kill_temp_logging,
)

kill_button = tk.Button(
    button_frame,
    text=f"STOP TEST",
    command=kill,
    fg='red',   
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

# slightly changed run function, instead of run button starting the shockcart run process
# make a function that runs the run_button functtion but also sets a flag so that we can start a timer



####################/BUTTONS/############################

################# STATUS WINDOW ######################

display_temp_label = tk.Label(
    info_frame, 
    textvariable=temp_data,
    relief="ridge",
)

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

timer_label = tk.Label(
    info_frame,
    textvariable=timer_num,
)

def update_temp_data():
    # read_temp_test not working because bitchass therm plate
    #new_data = cart1.read_temp_test()
    
    # using daq board and adc
    new_data = cart1.convertTemp()
    temp_data.set("UUT Temp\n"+str(f"To MUT:{new_data[0]}\nFrom MUT:{new_data[1]}"))
    app.after(3000,update_temp_data)

def update_run_status():
    if run_flag.get():
        run_var.set(f"Test In Progress")
        run_label.config(fg='green')
    else:
        run_var.set("Test Inactive")
        run_label.config(fg='red')
    app.after(1000,update_run_status)
         
def update_counter():
    new_counter_num = cart1.get_counter()
    counter_num.set(f"Cycle Count\n{new_counter_num}/{cart1.cycle_count}")
    app.after(1000,update_counter)

def update_timer():
    total_run_time = (cart1.cycle_time * 2) * cart1.cycle_count 
    if run_flag.get(): # if the run flag was set to true
        timer_num.set(f"Timer\n{cart1.test_time()}/{total_run_time}")
    else: # just put 0 minutes out of cycle_time minutes
        timer_num.set(f"Timer\n0/{cart1.cycle_time}")
    app.after(1000,update_timer)
    
################# /STATUS WINDOW/ ######################

##################HELPERFUNCTIONS###################
def get_position(app, widget): # function takes the app/root position and then add where the x starts, same for y, 
    x = app.winfo_rootx() + widget.winfo_x()
    y = app.winfo_rooty() + widget.winfo_y()
    print(f"get positon function\napp position x:{app.winfo_rootx()} y:{app.winfo_rooty()}\nwidget position x:{widget.winfo_x()} y:{widget.winfo_y()}")
    return (x, y)
    
def get_size(widget):
    x = widget.winfo_width()
    y = widget.winfo_height()
    print(
        f"get size function\n",
        f"name: {widget}\nx:{x} y:{y}",
    )
    return (x,y)

def update_pad_buttons():
    bit_list = cart1.relay_status()
    button_list = [co1,cb2,ci3,hb4,hi5,ho6,pump_7,fan_8]
    for index in range(len(bit_list)):
        # 0th index!!
        if bit_list[index] == '1':
            button_list[index].config(bg='green')
        else:
            button_list[index].config(bg='light grey')
    app.after(1000,update_pad_buttons)
    
def update_command():
    # going to just brute force this one
    # manually set each button to its relay
    # IF NOT RUNNING TEST
    # bug for relay 3, might as well loop through index 0-7 and check relay state list and toggle that way
    if not run_flag.get():
        co1.config(command=lambda:cart1.toggle_relay(1))
        cb2.config(command=lambda:cart1.toggle_relay(2))
        
        hb4.config(command=lambda:cart1.toggle_relay(4))
        hi5.config(command=lambda:cart1.toggle_relay(5))
        ho6.config(command=lambda:cart1.toggle_relay(6))
        pump_7.config(command=lambda:cart1.toggle_relay(7))
        fan_8.config(command=lambda:cart1.toggle_relay(8))
        
        # relay 3 doesn't toggle...
        # so i need to query the state for this one relay,
        # freakin bummer
        ci3.config(command=lambda:cart1.manual_toggle(3))
    app.after(1000,update_command)

def on_exit():
    cart1.hard_reset()
    app.destroy()
####################PADFRAME#######################

def connect_objects(b1, b2):
    # connect line between button 1 and button 2
    # calculate center point of button
    b1_center = (b1.winfo_x() + b1.winfo_width() / 2, b1.winfo_y() + b1.winfo_height() / 2)
    b2_center = (b2.winfo_x() + b2.winfo_width() / 2, b2.winfo_y() + b2.winfo_height() / 2)
    #print(f"Button 1 coords:{b1_center}\nButton 2 coords:{b2_center}") # shows the coords 
    
    # draw line
    pad_canvas.create_line(b1_center, b2_center)    
    
# follow scheme of numbering
    # cold_out = 1
    # cold_bypass = 2
    # cold_in = 3
    # hot_bypass = 4
    # hot_in = 5
    # hot_out = 6
    # pump = 7
    # fan = 8
pad_label = tk.Label(pad_canvas,text="Relay Control Pad",font=("Helvetica", 16, "bold"))
co1 = tk.Button(pad_canvas,text="Cold Outlet")
cb2 = tk.Button(pad_canvas,text="Cold Bypass")
ci3 = tk.Button(pad_canvas,text="Cold In")
hb4 = tk.Button(pad_canvas,text="Hot Bypass")
hi5 = tk.Button(pad_canvas,text="Hot In")
ho6 = tk.Button(pad_canvas,text="Hot Out")

# not in the flow (ish) diagram layout, will be set aside in the frame
pump_7 = tk.Button(pad_canvas,text="Pump")
fan_8 = tk.Button(pad_canvas,text="Fan")

# helper labels to draw lines
junc_to_mut = tk.Label(pad_canvas,text="TEE")
junc_from_mut = tk.Label(pad_canvas, text="TEE")
mut_outlet = tk.Label(pad_canvas, text="MUT Outlet")
mut_inlet = tk.Label(pad_canvas, text="MUT Inlet")




####################/PADFRAME/#######################

##########STATUS#############
info_frame.place(x=0,y=0)
info_frame.pack_propagate(False)
status_label.pack()
run_label.pack()
display_temp_label.pack()
update_run_status()
update_temp_data()
counter_label.pack()
timer_label.pack()
update_counter()
update_timer()
##########/STATUS/#############

##############BUTTONS###########
button_frame.place(x=0,y=200)
button_frame.pack_propagate(False)
run_button.pack()
kill_button.pack()
#hot_loop_button.pack()
#cold_loop_button.pack()
reset_relay_button.pack()
fill_button.pack()
# i ran out of room, need to restructure gui
# run test will start log
log_button.pack()
stop_log.pack()
##############/BUTTONS/###########

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
#  fan                                                              #    
#  pump                              CO                             #
#####################################################################
####PAD#GRID##########
#test_button.pack()
# arranging in order of column upper left to lower right
pad_canvas.place(x=190,y=0)
pad_canvas.grid_propagate(False) # helps with grid resizing 

pad_label.grid(row=1,column=6, sticky='ew') # sticky east/west means the widget will stretch horizantally to fill the space provided 500X300 ish
pad_canvas.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12), weight=1)
pad_canvas.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12), weight=1)

# grid placement
# hot side
hb4.grid(row=4, column=1, sticky='ew')
ho6.grid(row=3, column=2, sticky='ew')
hi5.grid(row=5, column=3, sticky='ew')
# cold side
co1.grid(row=8, column=6, sticky='ew')
cb2.grid(row=7, column=10, sticky='ew')
ci3.grid(row=6, column=7, sticky='ew')

pump_7.grid(row=1, column=1, sticky='ew')
fan_8.grid(row=1, column=2, sticky='ew')

mut_outlet.grid(row=3,column=10, sticky='ew')
mut_inlet.grid(row=5, column=10, sticky='ew')

junc_to_mut.grid(row=3, column=7,)
junc_from_mut.grid(row=5, column=6,)

# have to update the app before trying to get the coords 
app.update()
# after update get the positions off the windows so i can psotion them better

# test positioning
# print(get_position(app,pad_canvas))
# print(get_position(app,button_frame))
# print(get_position(app,pad_canvas))
# print(get_size(button_frame))
# print(get_size(pad_canvas))
# print(get_size(info_frame))

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

# test relay status
update_pad_buttons()
update_command()

###########TERMINAL###############
terminal_frame.place(x=0,y=400)
window_id = terminal_frame.winfo_id()
# print(window_id) # returns id for graphical object that we can bind xterm to, how neat 
os.system('xterm -fg "black" -fa "Monospace" -fs 12 -bg "#808080" -into %d -geometry 900x150 -sb &' % window_id)

try:
    app.title('Shockcart')
    app.protocol("WM_DELETE_WINDOW",on_exit) # set the exit strategy
    app.mainloop()
    
except KeyboardInterrupt:
    cart1.relay_plate_reset()
    

