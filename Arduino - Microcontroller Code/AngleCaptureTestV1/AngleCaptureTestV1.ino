int testvariable = 1;
int val = 0;


void setup() {
  Serial.begin(115200);
}

void loop() {
  if(testvariable >= 550){
    testvariable = 450;
  }
  else{
    testvariable = testvariable + 1;
  }
  val = testvariable;
  Serial.print("<");
  Serial.print(val);
  Serial.println(">");
  delay(200);
}

void serialEvent(){
  Serial.println("It worked!");
  }
