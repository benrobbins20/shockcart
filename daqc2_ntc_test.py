import piplates.DAQC2plate as d2
from time import sleep
from math import log

# corresponds to pin number from analog input pins on daq


temp_dict = {"To MUT":[d2.getADC(0,0),],"From MUT":[d2.getADC(0,1),]}
#adcDict = {"Cold inlet":int(temp_dict["Cold inlet"]*255/3.3),"MUT outlet":int(temp_dict["MUT outlet"]*255/3.3),"Heater Outlet":int(temp_dict["Heater Outlet"]*255/3.3)} # maybe a weird float conversion in there or something but its clse enough 

def calcADC(voltage):

    
    return (int(voltage*255/3.3)) # convert voltage back to adc value, which piplate does automatically
    



def convertTemp(temp_dict): # takes sensor dictionary as arg
    if not isinstance(temp_dict,dict):
        return
    # rt = (10*voltage) / (3.3 - voltage)
    # rt = (10000*adcValue) / (maxADC)
    # both of these will work and are accurate!!
    # since daq plate already grabs the voltage it should be used
    for item in temp_dict:
        # for key name in dictionary
        voltage = temp_dict[item][0]
        thermResistance = float((10*voltage) / (3.3 - voltage))
        tempK = 1/(1/(273.15+25) + log(thermResistance/10)/3950)
        tempC = round(tempK - 273.15,3)
        temp_dict[item].append(tempC)
    return temp_dict





# calcADC(temp_dict) # for funsies, this is optional
# #print(temp_dict)
# print(convertTemp(temp_dict))

print(convertTemp(temp_dict))






