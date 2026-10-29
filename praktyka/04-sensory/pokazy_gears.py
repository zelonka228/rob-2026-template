# Робота 4: покази кольору й ультразвуку в русі через заборонену зону.
# Світ: kursova/scena/custom_world_tyzhden4.json (Worlds -> Load from file).
# Робот розвертається на 180° і їде на південь через зону (20, -150).

import time
from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sensor.virtual import *

tank = MoveTank(OUTPUT_A, OUTPUT_B)
color = ColorSensor(INPUT_1)
ultra = UltrasonicSensor(INPUT_2)
gyro = GyroSensor(INPUT_3)
gps = GPSSensor(INPUT_4)
time.sleep(0.5)

# розворот на південь (гіроскоп 180°)
gyro.reset()
tank.on(20, -20)
while gyro.angle < 180:
    pass
tank.off()
time.sleep(1)
print("heading", gyro.angle, "start", round(gps.x, 1), round(gps.y, 1))

# новий рядок щоразу, коли робот проїхав >= 5 см (за GPS),
# print у циклі не використовую: він сповільнює симулятор
data = []
last = gps.y + 100
tank.on(30, 30)
while len(data) < 48:
    y = gps.y
    if abs(y - last) >= 5:
        data.append((len(data) + 1, round(gps.x, 1), round(y, 1),
                     color.reflected_light_intensity,
                     round(ultra.distance_centimeters, 1)))
        last = y
    if ultra.distance_centimeters < 7:
        break
    time.sleep(0.02)
tank.off()

# № x y колір відстань
for d in data:
    print(d[0], d[1], d[2], d[3], d[4])
