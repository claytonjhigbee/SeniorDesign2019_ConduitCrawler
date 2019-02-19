int testvariable = 1;
int val = 0;


void setup() {
  Serial.begin(9600);
}

void loop() {
  if(testvariable >= 180){
    testvariable = 1;
  }
  else{
    testvariable = testvariable + 1;
  }
  val = testvariable;
Serial.print(val);
Serial.print(" ");
Serial.print(val);
Serial.print("\n");
delay(25);
}
