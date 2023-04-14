# shockcart file with Shockcart() class
from w1thermsensor import W1ThermSensor
import piplates.RELAYplate2 as r2
import piplates.DAQC2plate as d2
import piplates.THERMOplate as th
from time import sleep

class Shockcart():

    def __init__(self): # no other args except for self, meaning a simple shockcart instance looks like cart1 = Shockcart()
        # init stuff define general parameters that we'll need

        # piplate id
        #daqc2_plate = channel 0
        #relay_plate2 = channel 1

        # relay id
        self.cold_out = 1
        self.cold_bypass = 2
        self.cold_in = 3
        self.hot_bypass = 4
        self.hot_in = 5
        self.hot_out = 6
        self.pump = 7
        self.fan = 8

        # example of verbose relay input
        # r2.relayON(relay_plate2, cold_out)
        # its simple to memorize board numbers 
        # can substitute 0 or 1 instead its just a helper 

    def fill(self,enable):
        # fill is going to go IN through the COLD_OUTLET
        # this way the majority of the lines get filled
        if enable:
            r2.relayON(1,self.cold_out)
            r2.relayON(1,self.hot_in)
            r2.relayON(1,self.hot_out)
        # reset all after enable boolean is disabled
        else:
            r2.RESET(1)
            return
    def relay_plate_reset(self):
        r2.RESET(1)
        



cart1 = Shockcart()


cart1.fill(True)
cart1.fill(False)

            
            
            




        
