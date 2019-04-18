int testvariable = 1;
int val = 0;


void setup() {
  Serial.begin(115200);
}

void loop() {
  if(testvariable >= 135){
    testvariable = 45;
  }
  else{
    testvariable = testvariable + 1;
  }
  val = testvariable;
Serial.println(val);
delay(25);
}

void serialEvent(){
  Serial.println("It worked!");
  }
