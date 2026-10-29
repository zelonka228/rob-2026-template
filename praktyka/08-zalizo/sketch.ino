// Робота 8: той самий поріг 15 см, схема Arduino Uno + датчик відстані (4 виводи).
const int TRIG = 9;
const int ECHO = 10;
const int LED = 13;
const int PORIH = 15;                 // см, той самий, що в Gears

void setup() {
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
  pinMode(LED, OUTPUT);
  Serial.begin(9600);
}

long vidstanSm() {
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);           // імпульс 10 мкс
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  long mks = pulseIn(ECHO, HIGH, 30000);   // чекати відлуння не довше 30 мс
  if (mks == 0) return -1;                  // відлуння не повернулось
  return mks / 58;                          // 58 мкс ≈ 1 см туди й назад
}

void loop() {
  long d = vidstanSm();
  Serial.print("d = ");
  Serial.print(d);
  Serial.println(" cm");
  digitalWrite(LED, (d >= 0 && d < PORIH) ? HIGH : LOW);
  delay(100);
}
