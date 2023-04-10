#include <wiringPi.h>
#include <stdio.h>
#include <math.h>
#include <ADCDevice.hpp>

ADCDevice *adc; // pointer to the ADCDevice class object

int main(void){
    adc = new ADCDevice(); // i guess new/delete is like malloc/free new/delete initialzes the memory space for an object also initilaizes in some way?
    printf("Start"); // comment for a print statement? ... yes. absolutely, print before loop, so only during init
    if(adc->detectI2C(0x4b)){ // think of this as the pointer variable adcmd pointing to class or structure detecti2c, meaning that is obviously part of a larger class, in ADCDevice header?
        // did verify that detecti2c is a function in .cpp file .hpp file 
        delete adc; //checks for and frees memory space reserved for adc class instance
        adc = new ADS7830();
        // i wanna like print what adc is now. is it an object of the ADCDevice() class now?
        //printf("%d",adc);
    }
    else{
        printf("Error"); //
        return -1;
    }
    
   while(1){
        int adcValue = adc->analogRead(0);  //read analog value A0 pin    
        float voltage = (float)adcValue / 255.0 * 3.3;    // calculate voltage, so confused should be (adc/255) * 3.3 but shat results in the wrong voltage
        float Rt = 10 * voltage / (3.3 - voltage);        //calculate resistance value of thermistor
        float tempK = 1/(1/(273.15 + 25) + log(Rt/10)/3950.0); //calculate temperature (Kelvin)
        float tempC = tempK -273.15;        //calculate temperature (Celsius)
        printf("%d\n",adcValue);
        //printf("%.2f",voltage);
        delay(100);
    }
    return 0;

}

