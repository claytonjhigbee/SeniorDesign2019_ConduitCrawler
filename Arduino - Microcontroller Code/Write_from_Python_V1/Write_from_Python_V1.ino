volatile int incomingByte = 0;
void setup() {
  Serial.begin(115200);

}

void loop() {
  incomingByte = Serial.read();
  // say what you got:
  Serial.print("I received: ");
  Serial.println(incomingByte, DEC);
  delay(10);
}
