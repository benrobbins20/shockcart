# shockcart file with Shockcart() class
import piplates.RELAYplate2 as r2
import piplates.DAQC2plate as d2
import piplates.THERMOplate as th

import threading, multiprocessing, time


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
        self.counter = 1
        self.cycle_count = cycle_count
        self.cycle_time = cycle_time # this defaults to 30 minutes and shouldn't need to change anything

        self.process = multiprocessing.Process(target=self.run_loop)
        
        # define an instance variable for the test start time
        # define it here but dont assign it to time.time() yet
        self.start_time = 0

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
        r2.RESET(1)
        if enabled:
            r2.relayON(1,self.hot_in)
            r2.relayON(1,self.hot_out)
            r2.relayON(1,self.cold_bypass)
        else:
            r2.relayOFF(1,self.hot_in)
            r2.relayOFF(1,self.hot_out)
            r2.relayOFF(1,self.cold_bypass)
                
    def cold_loop_enable(self,enabled = False): # default to off
        r2.RESET(1)
        if enabled:
            r2.relayON(1,self.cold_in)
            r2.relayON(1,self.cold_out)
            r2.relayON(1,self.hot_bypass)
        else:
            r2.relayOFF(1,self.cold_in)
            r2.relayOFF(1,self.cold_out)
            r2.relayOFF(1,self.hot_bypass)

    def convert_seconds(self,minutes):
        #print(minutes)
        if not minutes:
            minutes = self.cycle_time
        seconds = minutes * 60
        #print(seconds)
        return seconds
    
    def create_timer(self):
        # when called start time is set to current time
        # can call this function inside the while loop of the run_loop to reset the counter
        self.start_time = time.time()

    def test_time(self):
        # need a function that has an updating but verbose timer that shows minutes:seconds and updates every second
        elapsed = time.time() - self.start_time
        minutes = int(elapsed // 60) # seconds may be < 60 how many times does seconds go into 60, integer rounding DOWN
        seconds = int(elapsed % 60) # seconds can go into 60 with how much remainder, aka excluding minutes
        return (f"{minutes}:{seconds}")
        
    def relay_status(self):
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
    
    def full_bypass(self,enabled=False):
        if enabled:
            r2.RESET(1)
            r2.relayON(1,self.hot_bypass)
            r2.relayON(1,self.cold_bypass)
        else:
            r2.relayOFF(1,self.hot_bypass)
            r2.relayOFF(1,self.cold_bypass)
            
    def all_on(self):
        r2.RESET(1)
        r2.relayALL(1,255)
        
    def all_off(self):
        r2.RESET(1)

    def run_loop(self):
        sec = self.convert_seconds # so you can like locally rename a self.object in a function for compact function calls
        cycle_time = self.cycle_time
        self.test_start_time = 0
        while self.counter <= self.cycle_count:
            print(f"while start\nCounter={self.counter}/{self.cycle_count}") 

            ####HOT##############
            self.hot_loop_enable(True)
            print("HOT wait 5 seconds")
            time.sleep(5) # wait 5 seconds before turning on pump
            r2.relayON(1,self.pump) # check manual switch
            time.sleep(sec(cycle_time))  
            r2.relayOFF(1,self.pump) # turn pump off after cycle time
            self.hot_loop_enable(False) # disable hot loop
            self.full_bypass(True) # open both bypasses

            ##########COLD##############
            self.cold_loop_enable(True)
            print("COLD: wait 5 seconds")
            time.sleep(5)
            r2.relayON(1,self.pump) # hot bypass is enabled can resume hot loop 
            time.sleep(sec(cycle_time))
            r2.relayOFF(1,self.pump)
            self.full_bypass(True)
            self.hot_loop_enable(False)
            
            # increment counter 
            self.counter += 1
        # this will execute after cycle completes
        self.full_bypass()
        print("while loop done")

    def run_loop_process(self):
        if not self.process.is_alive():
            print("starting process")
            self.process.start()

    def kill_loop_process(self):
        if self.process.is_alive():
            print('killing process')
            self.process.terminate()
            self.relay_plate_reset()

    def read_temp_test(self):
        chan1= f"Channel 1: {str(th.getTEMP(2,1))} C"
        chan2 = f"Channel 2: {str(th.getTEMP(2,2))} C"
        return chan1, chan2

    def get_counter(self,):
        return self.counter
    
    def toggle_relay(self,num):
        r2.relayOn(1,num)
        
# #testing

# cart1 = Shockcart(3,3)
# print(cart1.read_temp_test())