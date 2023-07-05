import can
import cantools
from cantools.database import DecodeError
import cantools.database.can.signal as cansig
import os



def load_dbc():
    # Loads all DBCs from the folder 'dbc' into the database
    # this is the method used by hwi/danfoss dyno app
    # was using load_file method instead of add_file
    # this adds all dbc's in a folder "./dbc"
    global db
    db = cantools.database.Database()
    for file in os.listdir('./dbc'):
        #print(file)
        if file.endswith('.dbc'):
            db.add_dbc_file('./dbc/'+file)

def createSocket(enabled=False):
    # create a bus instance with python-can library
    # MUST HAVE can0 interface up and started
    # pi is set up to do this automatically on boot
    # edit /etc/network/interfaces
    ###################
    # allow-hotplug can0
    # iface can0 inet manual
    # pre-up /sbin/ip link set $IFACE type can bitrate 500000
    # up /sbin/ifconfig $IFACE up
    # down /sbin/ifconfig $IFACE down
    ###################
    global bus
    if enabled:
        bus = can.interface.Bus("can0", bustype='socketcan')
    else:
        bus.shutdown()
        
def readInverterTemp():
    while True:
        try:
            message = bus.recv()
            # parse the name by using the frame_id and then pulling name attribute off that message
            message_name = db.get_message_by_frame_id(message.arbitration_id).name
            if message_name == "m1_Temperature":
                # find message by string name MUT 1 temperature
                temp_data = db.decode_message(message.arbitration_id,message.data)
                print(temp_data["tm_m1_Inverter"])
        except KeyError:
            # key error exception will result if arb_id is not on the canbus 
            pass
try:
    load_dbc()
    createSocket(True)
    readInverterTemp()
except KeyboardInterrupt:
    createSocket(False)
    