# Робота 6: поведінка як автомат станів.
# Частина місії № 2 з картки (ускладнення № 5): іти полем, не заїжджаючи
# в заборонену зону, і зупинитись за 15 см перед об'єктом.
# Світ: kursova/scena/custom_world_tyzhden6.json (старт (0, 60), розвернутий на південь).

from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor, GyroSensor
import time

tank = MoveTank(OUTPUT_A, OUTPUT_B)
color = ColorSensor(INPUT_1)
ultra = UltrasonicSensor(INPUT_2)
gyro = GyroSensor(INPUT_3)
time.sleep(0.5)

PORIH_ZONY = 40       # з роботи 4: нижче — заборонена зона
PORIH_PIDHID = 45     # см: ближче — їдемо повільно
PORIH_STOP = 20       # см: тут зупиняємо хід, далі точно доводимо
MIN_OK = 12           # з картки: 15 ± 3 см
MAX_OK = 18
TAIMAUT = 30          # с у одному стані
MAKS_ZON = 5          # більше заходів у зону — щось не так, зупиняємось
SHVYDKIST_POSHUK = 30  # % у стані poshuk; у роботі 9 міняю між прогонами

stan = "poshuk"
vkhid = time.time()   # коли увійшли в поточний стан
pochatok = time.time()  # старт прогону, для загального часу
zon = 0               # скільки разів спрацював стан zona


def perekhid(novyi):
    """Єдине місце, де змінюється стан: друк і дії при вході."""
    global stan, vkhid, zon
    print(f"{stan} -> {novyi}")
    stan = novyi
    vkhid = time.time()
    if novyi == "zona":
        gyro.reset()
        zon += 1


while stan != "gotovo":
    d = ultra.distance_centimeters
    c = color.reflected_light_intensity

    if stan == "poshuk":              # їдемо вперед
        tank.on(SpeedPercent(SHVYDKIST_POSHUK), SpeedPercent(SHVYDKIST_POSHUK))
        if c < PORIH_ZONY:
            perekhid("zona")
        elif d < PORIH_PIDHID:
            perekhid("pidhid")

    elif stan == "pidhid":            # наближаємось повільно
        tank.on(SpeedPercent(10), SpeedPercent(10))
        if c < PORIH_ZONY:
            perekhid("zona")
        elif d < PORIH_STOP:
            tank.off()
            perekhid("utochnennya")

    elif stan == "utochnennya":       # довести до 15 ± 3 см за реальною відстанню
        if time.time() - vkhid < 0.7:
            tank.off()                # дати моторам зупинитись
        elif d < MIN_OK:
            tank.on(SpeedPercent(-5), SpeedPercent(-5))
        elif d > MAX_OK:
            tank.on(SpeedPercent(5), SpeedPercent(5))
        else:
            tank.off()
            perekhid("gotovo")

    elif stan == "zona":              # назад із зони, потім поворот праворуч на 90°
        if time.time() - vkhid < 1.2:
            tank.on(SpeedPercent(-20), SpeedPercent(-20))
        else:
            tank.on(SpeedPercent(20), SpeedPercent(-20))
            if gyro.angle >= 90:
                tank.off()
                perekhid("poshuk")

    if time.time() - vkhid > TAIMAUT: # таймаут: стан без виходу
        print("таймаут у стані", stan)
        tank.off()
        break

    if zon > MAKS_ZON:                # глухий кут: poshuk <-> zona без кінця
        print("забагато заходів у зону")
        tank.off()
        break

tank.off()
print("зон оминув:", zon, "· відстань до об'єкта:", round(ultra.distance_centimeters, 1), "см · час:", round(time.time() - pochatok, 1), "с")
