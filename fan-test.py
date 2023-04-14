from w1thermsensor import W1ThermSensor
import piplates.RELAYplate2 as r2
sens1 = W1ThermSensor()
print(sens1.get_temperature())

while True:
    if sens1.get_temperature() > 30.0:
        r2.relayON(1,8)
    else:
        r2.RESET(1)


