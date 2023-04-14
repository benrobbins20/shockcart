import piplates.RELAYplate2 as r
import os, glob, time
from w1thermsensor import W1ThermSensor
import piplates.DAQC2plate as d2
import piplates.RELAYplate2 as r2


#enable one-wire modules
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


# find the directory
# i've never used glob but it would be nice to learn
# basic file path bullshit with os
def gen_devices():
    w1_base_dir = "/sys/bus/w1/devices"
    #print(os.listdir(w1_base_dir)) # provides list of files in the base_dir
    # ds18 device should start with '28'
    w1_list = os.listdir(w1_base_dir)
    device_list = []
    for i in w1_list:
        if i.startswith('28'):
            device_path = (os.path.join(w1_base_dir,i))
            device_list.append(device_path)
    return device_list
#print(gen_devices()) # returns list with all the device dirs 

def read_file(): # function returns a list of each individual line of the rom
    for folder in gen_devices():
        os.chdir(folder) # change to the correct folder
        #print(os.getcwd())
        name_file = open(folder + '/name','r')
        rom_file = open(folder + '/w1_slave', 'r')
        name_formatted = name_file.read().splitlines()
        rom_formatted = rom_file.read().splitlines()
        return [name_formatted,rom_formatted]
    

def parse_temp():
    lines = read_file()
    # perform "YES" check
    if lines: # if not there will be no sensor directory found, may have to bit bang
        while lines[1][0].strip()[-3:] == "YES":
            # print(f"YES check passed {lines[1][0]}")
            temp_line = lines[1][1]
            t_equals = temp_line.find("t=")
            temp = temp_line[t_equals+2:]
            temp_c = float(temp) / 1000
            temp_f = temp_c * 9.0 /5.0 + 32.0
            return [temp_c,temp_f]
        return # will quit silently if "YES" check fails
    else:
        print("Error: could not read sensor directory")
        return
#print(parse_temp()) # this is working at the moment

def running_temp(duration): # duration in seconds
    timer = 0
    while timer <= duration:
        print(f"Sensor {read_file()[0]}\nTemp Celsius: {parse_temp()[0]}\nTemp Fahrenheit: {parse_temp()[1]}\nCounter {timer}/{duration}")
        time.sleep(1.0)
        timer += 1


#running_temp(10)




# try the thermsensor library

sens1 = W1ThermSensor()

print(sens1.id) # hey it works

print(sens1.get_temperature())

#print(r2.getID(1))

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    