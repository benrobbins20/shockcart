# shockcart file with Shockcart() class
from w1thermsensor import W1ThermSensor
import piplates.RELAYplate2 as r2
import piplates.DAQC2plate as d2
import piplates.THERMOplate as th
from time import sleep
from threading import *


class Shockcart():
    #################
    #class variables will be standard to all instances
    cold_out = 1
    cold_bypass = 2
    cold_in = 3
    hot_bypass = 4
    hot_in = 5
    hot_out = 6
    pump = 7
    fan = 8
    
    def __init__(self,cycle_count,cycle_time=30): # no other args except for self, meaning a simple shockcart instance looks like cart1 = Shockcart()
        # init stuff define general parameters that we'll need

        # piplate id
        #daqc2_plate = channel 0
        #relay_plate2 = channel 1
        
        # you can access the class variables from the constructor or anywhere
        #print(self.pump)

        # example of verbose relay input
        # r2.relayON(relay_plate2, cold_out)
        # its simple to memorize board numbers 
        # can substitute 0 or 1 instead its just a helper 

        # cycle_time parameter is in minutes ie 30 minutes
        # cycle_count indicates how many cycles, a cycle is 1 hot and 1 cold 
        self.cycle_count = cycle_count
        self.cycle_time = cycle_count # this defaults to 30 minutes and shouldn't need to change anything
        

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

    def hot_loop_enable(self,enabled = False): # default to off
        if enabled:
            r2.relayON(1,self.hot_in)
            r2.relayON(1,self.hot_out)
            r2.relayON(1,self.cold_bypass)
        else:
            r2.relayON(1,self.hot_in)
            r2.relayON(1,self.hot_out)
            r2.relayON(1,self.cold_bypass)
            
        
    def cold_loop_enabled(self,enabled = False): # default to off
        if enabled:
            r2.relayON(1,self.cold_in)
            r2.relayON(1,self.cold_out)
            r2.relayON(1,self.hot_bypass)
        else:
            r2.relayOFF(1,self.cold_in)
            r2.relayOFF(1,self.cold_out)
            r2.relayOFF(1,self.hot_bypass)

    
    def convert_seconds(self):
        minutes = self.cycle_time
        seconds = minutes * 60
        return seconds
    
    def start_pump(self):
        # heres a fun one 
        # below is a list of pump run criteria
        # list of integers that can be interpreted as 8 bit binary 
        # we have 8 relays
        # we have 8 corresponding bits
        ##############EXAMPLE############
        # 
        # bypass relay is number 4
        # in binary -> 00001000
        # 4th relay bit is set to 1
        # all on 11111111
        # all off 00000000
        self.allow_pump = [8,]
        integer = (r2.relaySTATE(1))
        self.binary = format(integer, 'b')
        print(integer,self.binary)
    
    def full_bypass(self):
        r2.RESET(1)
        r2.relayON(1,self.hot_bypass)
        r2.relayON(1,self.cold_bypass)
    
    def all_on(self):
        r2.RESET(1)
        r2.relayALL(1,255)

    def run(self):
        self.counter = 1 
        while self.counter <= self.cycle_count:
            # by default will run hot loop first
            self.hot_loop_enable(True)
            sleep(5) # wait 5 seconds before turning on pump
            r2.relayON(1,self.pump) # check manual switch
            sleep(self.cycle_time)
            r2.relayOFF(1,self.pump)
            self.hot_loop_enable(False)
            self.cold_loop_enabled(True)
            sleep(5)
    
        self.counter += 1
        



        




cart1 = Shockcart(5)
#cart1.hot_loop_enable()
#cart1.all_on()
cart1.start_pump()  


            
            
            




        
