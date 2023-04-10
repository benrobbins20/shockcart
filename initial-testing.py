import piplates.RELAYplate2 as r2
from time import sleep

# verbose variables for relay integers
cold_bypass = 1
cold_in = 2
cold_out = 3
hot_in = 4
hot_out = 5
hot_bypass = 6

# define cold loop and hot loop functions
def hot_loop(cycle_time):
    r2.relayON(1,hot_in)
    r2.relayON(1,hot_out)
    r2.relayON(1,cold_bypass)
    sleep(cycle_time)
def cold_loop(cycle_time):
    r2.relayON(1,cold_in)
    r2.relayON(1,cold_out)
    r2.relayON(1,hot_bypass)
    sleep(cycle_time)
    

try:
    while True:
        # hot loop first
        hot_loop(30)
        r2.RESET(1)
        sleep(5)
        cold_loop(30)
        r2.RESET(1)
        sleep(5)
        
        
except KeyboardInterrupt:
    r2.RESET(1)

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        