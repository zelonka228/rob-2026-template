# Робота 3: 10 поворотів "на час" і 10 поворотів "по гіроскопу".
# Середовище: Gears, світ Grid, стандартний робот, швидкість 20 %, поворот праворуч.

from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor import INPUT_3
from ev3dev2.sensor.lego import GyroSensor
import time

tank = MoveTank(OUTPUT_A, OUTPUT_B)   # A — ліве колесо, B — праве
gyro = GyroSensor(INPUT_3)            # у Gears порт обов'язковий
time.sleep(0.5)

print("gyro:", gyro.angle)

# Розігрівальний поворот, у таблицю не йде
tank.on_for_seconds(SpeedPercent(20), SpeedPercent(-20), 1.0)
time.sleep(0.5)

# Крок 2: 10 поворотів "на час" (1 с, 20 %)
poperednii = gyro.angle
for i in range(1, 11):
    tank.on_for_seconds(SpeedPercent(20), SpeedPercent(-20), 1.0)
    time.sleep(0.5)
    teper = gyro.angle
    print("T", i, teper - poperednii)   # кут саме цього повороту
    poperednii = teper

# Крок 4: 10 поворотів "по гіроскопу" до 90°
for i in range(1, 11):
    gyro.reset()
    tank.on(SpeedPercent(20), SpeedPercent(-20))
    while gyro.angle < 90:
        pass
    tank.off()
    time.sleep(0.5)
    print("G", i, gyro.angle)

# Трек П: компенсація. Нова тривалість = 1.0 * 90 / середнє "на час" (75.4)
# і ті самі 10 поворотів:
#   TRYVALIST = 1.0 * 90 / 75.4      # 1.194 с
#   tank.on_for_seconds(SpeedPercent(20), SpeedPercent(-20), TRYVALIST)
