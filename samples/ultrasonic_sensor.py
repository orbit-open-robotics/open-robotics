#
# distance_sensor_test
#
# Pins
# ----
# 5V   - VCC
# GND  - GND
# GP21 - Echo
# GP20 - Trig
#
from time import sleep
from distance_sensor import DistanceSensor


distance_sensor = DistanceSensor(trig=20, echo=21)
while True:
    print(distance_sensor.get_distance_cm())
    sleep(0.1)

