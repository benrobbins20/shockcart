import tkinter as tk
from tkinter import ttk
from shockcart import Shockcart # bringing in the Shockcart class
cart1 = Shockcart() # instance of shockcart

# root window
root = tk.Tk()
root.geometry('300x200')
root.resizable(False, False)
root.title('Fill Cart')

# exit button
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

fill_button.pack(
    ipadx=5,
    ipady=5,
    expand=True
)

reset_relay_button.pack()

root.mainloop()