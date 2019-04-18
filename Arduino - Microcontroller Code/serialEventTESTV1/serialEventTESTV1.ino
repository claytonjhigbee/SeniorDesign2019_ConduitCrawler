void setup() {
  Serial.begin(115200);

}

void loop() {
  // put your main code here, to run repeatedly:

}

void serialEvent(){
  char hi = Serial.read();
  Serial.println("i read ");
  Serial.print(hi);
  Serial.print("\r");
  }
