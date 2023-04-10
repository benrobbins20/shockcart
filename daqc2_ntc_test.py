import piplates.DAQC2plate as d2
from time import sleep
from math import log

# corresponds to pin number from analog input pins on daq
coldInletPin = 0
mutOutletPin = 1
heaterOutletPin = 2

masterDict = {"Cold inlet":[d2.getADC(0,coldInletPin),],"MUT outlet":[d2.getADC(0,mutOutletPin),],"Heater Outlet":[d2.getADC(0,heaterOutletPin),]}
#adcDict = {"Cold inlet":int(masterDict["Cold inlet"]*255/3.3),"MUT outlet":int(masterDict["MUT outlet"]*255/3.3),"Heater Outlet":int(masterDict["Heater Outlet"]*255/3.3)} # maybe a weird float conversion in there or something but its clse enough 

def calcADC(masterDict):
    for item in masterDict:
        # item = key name
        voltage = masterDict[item][0] # have to grab the item in the list, which should be ind = 0
        masterDict[item].append(int(voltage*255/3.3)) # convert voltage back to adc value, which piplate does automatically
        



def convertTemp(masterDict): # takes sensor dictionary as arg
    if not isinstance(masterDict,dict):
        return
    # rt = (10*voltage) / (3.3 - voltage)
    # rt = (10000*adcValue) / (maxADC)
    # both of these will work and are accurate!!
    # since daq plate already grabs the voltage it should be used
    for item in masterDict:
        # for key name in dictionary
        voltage = masterDict[item][0]
        thermResistance = float((10*voltage) / (3.3 - voltage))
        tempK = 1/(1/(273.15+25) + log(thermResistance/10)/3950)
        tempC = round(tempK - 273.15,3)
        masterDict[item].append(tempC)
    return masterDict



calcADC(masterDict) # for funsies, this is optional
#print(masterDict)
print(convertTemp(masterDict))




