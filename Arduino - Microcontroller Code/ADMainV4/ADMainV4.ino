/*
  This code is used to control the DC servo motors for the Conduit Crawler
  It initializes the pin positions for control from the Microcontroller and 
  impliments a simple forward drive motion. The code interfaces with the
  L298N Motor Controller Board. Our project uses the same control signals to
  operate two controller boards with a total of 4 DC motors.
  analogWrite() functions determines the spead of the DC motors
  The follwing tables controls the operation of the Hbridge. Setting the 
  related pins will provide the desired direction
IN1   IN2   IN3   IN4   Direction
0     0     0     0     Stop
1     0     1     0     Forward
0     1     0     1     Reverse
1     0     0     1     Left
0     1     1     0     Right
 
 */

//Motor Connections and definitions
//The Arduino Pins on left, AVR pins on right
#define EnA 10 // PB2
#define EnB 5 // PD5
#define In1 11 // PB3 was 9 PB1
#define In2 8 // PB0
#define In3 7 // PD7
#define In4 6 // PD6
#define FBServo 9 // PB1
volatile int pwm_value = 0;
volatile int prev_time = 0;
volatile String incomingFlag;
volatile int count = 0;
 
void setup()
{
  Serial.begin(115200);
  Serial.setTimeout(1);
  // when pin D2 goes high, call the rising function
  attachInterrupt(0, rising, RISING);
  // All motor control pins are outputs
  pinMode(EnA, OUTPUT); // PWM Signal of duty cycle between 0 (always off) and 255 (always on), accepts integers
  pinMode(EnB, OUTPUT); // PWM Signal "                                                                        "
  pinMode(In1, OUTPUT);
  pinMode(In2, OUTPUT);
  pinMode(In3, OUTPUT);
  pinMode(In4, OUTPUT);
  pinMode(FBServo, OUTPUT);
}

void goForward()   //run both motors forward in the same direction
{
  digitalWrite(In1, HIGH);
  digitalWrite(In2, LOW);
  digitalWrite(In3, HIGH);
  digitalWrite(In4, LOW);
  digitalWrite(EnA, HIGH);
  digitalWrite(EnB, HIGH);
  
}

void goBackward()   //run both motors backward in the same direction
{
  // turn on motor A
  digitalWrite(In1, LOW);
  digitalWrite(In2, HIGH);
  // set speedA to 150 out 255
  analogWrite(EnA, 200);
  // turn on motor B
  digitalWrite(In3, LOW);
  digitalWrite(In4, HIGH);
  // set speedB to 150 out 255
  analogWrite(EnB, 200);
  delay(2000);
  // now turn off motors
  digitalWrite(In1, LOW);
  digitalWrite(In2, LOW);  
  digitalWrite(In3, LOW);
  digitalWrite(In4, LOW);
}

void Stop()   //Stop Motors
{
  digitalWrite(In1, LOW);
  digitalWrite(In2, LOW);
  digitalWrite(In3, LOW);
  digitalWrite(In4, LOW);  
}

void RunServo(){
  analogWrite(FBServo,175);
if (pwm_value >= 575)
{
  analogWrite(FBServo,0);
  }
  delay(70);
analogWrite(FBServo,200);
if (pwm_value <= 525)
{
  analogWrite(FBServo,0);
  }
  delay(70);
}

  
void loop()
{
  incomingFlag = Serial.readString();
  if (incomingFlag == "S"){
   while (count < 20){
    Stop();
    Serial.println("Motor Stopped");
    RunServo();
    count = count + 1;
   }
   count = 0;
  }
  //goForward();
  RunServo();
}

void rising() {
  attachInterrupt(0, falling, FALLING);
  prev_time = micros();
}
 
void falling() {
  attachInterrupt(0, rising, RISING);
  pwm_value = micros()-prev_time;
  Serial.println(pwm_value);
}
