#!/usr/bin/env python3
# Робота 2, програма 1: їхати вперед і зупинитись за 15 см до перешкоди.
# Середовище: Gears (Ev3dev-режим), ультразвуковий датчик на порту 2.

import time
from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sensor.virtual import *

tank = MoveTank(OUTPUT_A, OUTPUT_B)
ultra = UltrasonicSensor(INPUT_2)
THRESHOLD = 15  # см

# tank.on() не чекає, тому в циклі можна читати датчик, поки робот їде
# (on_for_seconds() тут не годиться: поки воно працює, датчик не читається)
tank.on(30, 30)
while ultra.distance_centimeters > THRESHOLD:
    time.sleep(0.01)
tank.off()
time.sleep(1)
print('stop distance', ultra.distance_centimeters)
