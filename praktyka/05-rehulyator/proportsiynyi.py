# Робота 5: рух за лінією, пропорційний регулятор.
# Gears, світ Line Following Challenges -> Simple Curves.
# Датчик кольору на порту 1, GPS на порту 4 (лише секундомір на фініші).

from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.virtual import GPSSensor
import time

tank = MoveTank(OUTPUT_A, OUTPUT_B)
color = ColorSensor(INPUT_1)
gps = GPSSensor(INPUT_4)
time.sleep(0.5)

PORIH = 55   # біле 100, лінія 13: (100 + 13) / 2 ≈ 56
BAZA = 20
Kp = 0.5     # міняти від запуску до запуску


def obmezhyty(v):
    # SpeedPercent поза ±100 у Gears падає з ValueError
    return max(-100, min(100, v))


pochatok = time.time()
while time.time() - pochatok < 120 and gps.y < 85:
    v = color.reflected_light_intensity
    e = PORIH - v
    korekciya = Kp * e
    tank.on(SpeedPercent(obmezhyty(BAZA - korekciya)),
            SpeedPercent(obmezhyty(BAZA + korekciya)))

tank.off()
print("Kp", Kp, "час до кінця траси: %.1f с" % (time.time() - pochatok))
