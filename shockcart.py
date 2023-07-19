# shockcart file with Shockcart() class
import piplates.RELAYplate2 as r2
import piplates.DAQC2plate as d2
import piplates.THERMOplate as th

import threading, multiprocessing, time, csv
from datetime import datetime


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
        # daqc2_plate = channel 0
        # relay_plate2 = channel 1
        # thermoplate2 = channel 2
        
        # you can access the class variables from the constructor or anywhere
        #print(self.pump)

        # example of verbose relay input
        # r2.relayON(relay_plate2, cold_out)
        # its simple to memorize board numbers 
        # can substitute 0 or 1 instead its just a helper 
        # probably never use 

        # cycle_time parameter is in minutes ie 30 minutes
        # cycle_count indicates how many cycles, a cycle is 1 hot and 1 cold 
        self.counter = 1
        self.cycle_count = cycle_count
        self.cycle_time = cycle_time # this defaults to 30 minutes and shouldn't need to change anything

        self.process = multiprocessing.Process(target=self.run_loop)
        self.log_proc = multiprocessing.Process(target=self.temp_logger)
        
        self.log_file_path = f"/home/sparky/shockcart/{self.set_datetime()}.csv"
        
        # define an instance variable for the test start time
        # define it here but dont assign it to time.time() yet
        self.start_time = 0
        self.relay_state_list = []

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
        # would like to leave fan on all the time when a test is running but I'm out of buttons, damn
        # just use a loop for now 
        for i in range(1,8):
            # excludes 8
            r2.relayOFF(1,i)

    def hard_reset(self):
        r2.RESET(1)
            
    def hot_loop_enable(self,enabled = False): # default to off
        self.relay_plate_reset()
        if enabled:
            r2.relayON(1,self.hot_in)
            r2.relayON(1,self.hot_out)
            r2.relayON(1,self.cold_bypass)
        else:
            r2.relayOFF(1,self.hot_in)
            r2.relayOFF(1,self.hot_out)
            r2.relayOFF(1,self.cold_bypass)
                
    def cold_loop_enable(self,enabled = False): # default to off
        self.relay_plate_reset()
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
    
    def set_time(self):
        # when called start time is set to current time
        # can call this function inside the while loop of the run_loop to reset the counter
        self.start_time = time.time()

    def test_time(self):
        # need a function that has an updating but verbose timer that shows minutes:seconds and updates every second
        elapsed = time.time() - self.start_time
        minutes = int(elapsed // 60) # seconds may be < 60, how many times does seconds go into 60, integer division, rounding DOWN
        seconds = int(elapsed % 60) # seconds can go into 60 with how much remainder, aka excluding minutes
        return (f"{minutes}:{seconds}")
        
    def relay_status(self):
        # heres a fun one 
        # list of integers that can be interpreted as 8 bit binary 
        # we have 8 relays
        # we have 8 corresponding bits
        
        ##############EXAMPLE############
        # bypass relay is number 4
        # in binary -> 00001000
        # 4th relay bit is set to 1
        # all on 11111111
        # all off 00000000
        # REVERSE THE ORDER OF THE STRING FOR MY SANITY
        # relay 4 will be 00010000
        ########/EXAMPLE/###########
        
        self.relay_state_list = [] # clear the list before calling it again
        integer = (r2.relaySTATE(1)) # pi-plates annoyingly returns intger for state
        binary = format(integer, 'b') # convert integer to 8 bit binary representation
        
        # quickie string reversal
        # this means [start index:endindex:how we are skipping]
        # empty means implied index, so [first index:last index:move backwards one index at a time] 
        binary = binary[::-1] # turn the bits around to reflect relays 1-8, 
        while len(binary) < 8: # only shows bits up until the last bit engaged
            binary = binary + '0' # just add string '0' until length is 8
            # DOES NOT RUN IF 8th BIT IS SET!! which is our fan we might just run that the whole time
        for bit in binary:
            self.relay_state_list.append(bit)
        return self.relay_state_list
    
    def full_bypass(self,enabled=False):
        if enabled:
            r2.RESET(1)
            r2.relayON(1,self.hot_bypass)
            r2.relayON(1,self.cold_bypass)
        else:
            r2.relayOFF(1,self.hot_bypass)
            r2.relayOFF(1,self.cold_bypass)
            
    def set_datetime(self):
        current_datetime = datetime.now()
        return current_datetime.strftime('%Y%m%d%I%M')
    
    def temp_logger(self):
        headers = ["Time","InletTemp","OutletTemp"]
        while True:
            with open(self.log_file_path, 'a',newline='') as logfile:
                write_csv = csv.writer(logfile)
                if logfile.tell() == 0:
                    write_csv.writerow(headers)
                    # means if when you open the file and the tell pointer is at 0, then the file is empty (because its at position 0 when entering)
                    # can use whole integers because tell is reflection of the acutal byte/binary position of the pointer/cursor
                    # if tell equals 0 then we can add the headers to the file 
                    
                write_csv.writerow([time.ctime(), self.read_temp_test()[0],self.read_temp_test()[1]]) # write corresponding data from thise list to the headers list
            
            time.sleep(5)
            
    def temp_logger_process(self):
        if not self.log_proc.is_alive():
            self.log_proc.start()
                
    def kill_temp_logging(self):
        self.log_proc.terminate()
        
    def all_on(self):
        r2.RESET(1)
        r2.relayALL(1,255)
        
    def all_off(self):
        r2.RESET(1)

    def run_loop(self):
        sec = self.convert_seconds # so you can like locally rename a self.object in a function for compact function calls
        cycle_time = self.cycle_time
        while self.counter <= self.cycle_count:
            self.set_time() # reset the time to current time before every cycle
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
            self.start_time = time.time()
            print("starting process")
            self.process.start()

    def kill_loop_process(self):
        if self.process.is_alive():
            print('killing process')
            self.process.terminate()
            self.relay_plate_reset()

    def read_temp_test(self):
        th.setTYPE(2,1,'k')
        th.setTYPE(2,2,'k')
        return [th.getTEMP(2,1), th.getTEMP(2,2)]

    def get_counter(self):
        return self.counter
    
    def toggle_relay(self,num):
        r2.relayTOGGLE(1,num)
        #print(self.relay_status())
    
    def manual_toggle(self,num):
        if self.relay_status()[num-1] == '0':
            r2.relayON(1,num)
        elif self.relay_status()[num-1] == '1':
            r2.relayOFF(1,num)
        
        
# #testing

#cart1 = Shockcart(3,3)
# print(cart1.read_temp_test())
#print(cart1.relay_status())
#r2.relayTOGGLE(1,5)
#r2.relayTOGGLE(1,3)
#r2.relayTOGGLE(1,all)



