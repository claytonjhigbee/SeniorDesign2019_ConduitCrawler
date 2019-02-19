volatile int pwm_value = 0; // Assign these two variables as volatile variables
volatile int prev_time = 0;

int servo = 9;    // FBServo connected to digital pin 9
boolean button = 11;
int analog = 180;

/*
Parameters
*/

void setup() {
  pinMode(button,INPUT);
  pinMode(servo,OUTPUT);
  Serial.begin(9600); //Begin Serial Monitor into /dev/ttyACM0
  // when pin D2 goes high, call the rising function
  attachInterrupt(0, rising, RISING);
  analog = 0;
  analogWrite(servo, analog); //Initial direction command for servo
}

void loop() {
analogWrite(servo,175);
if (pwm_value >= 500)
{
  analogWrite(servo,0);
  }
  delay(75);
analogWrite(servo,200);
if (pwm_value <= 400)
{
  analogWrite(servo,0);
  }
  delay(75);


//if (pwm_value <= 400){
//    analogWrite(servo,175);
//}
//else{
//analogWrite(servo,0);
//}
//
//if (pwm_value >= 300){
//    analogWrite(servo,197);
//}
//else{
//analogWrite(servo,0);
//}
}



void rising() {
  attachInterrupt(0, falling, FALLING);
  prev_time = micros();
} 


void falling() {
  attachInterrupt(0, rising, RISING);
  pwm_value = micros()-prev_time;
  Serial.print(pwm_value);
  Serial.print(" ");
  Serial.print(pwm_value);
  Serial.print("\n");
}
