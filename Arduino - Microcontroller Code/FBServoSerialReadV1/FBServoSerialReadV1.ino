
/*
This code is used to find out the length of a PWM signal using interrupts 
on Digital Pin 2 (PD2 - Atmega328) and writes the value to the Serial Monitor.

The program initializes communication to the serial port and then waits for an
interrput to occur on the pin. It then keeps track of time between the falling
and rising edges of the signal to then calculate PWM signal.

[Output is between 0-1024]
In our case, those values relate to certain angle relative to the internal
potentiometer of hte Feedback Servo Motor. 

About Volatile:
A variable should be declared volatile whenever its value can be changed by 
something beyond the control of the code section in which it appears, such 
as a concurrently executing thread. In the Arduino, the only place that this 
is likely to occur is in sections of code associated with interrupts, 
called an interrupt service routine (ISR).

This program only uses PD2
Device requires nominal voltage of 6V
*/
volatile int pwm_value = 0;
volatile int prev_time = 0;
 
void setup() {
  Serial.begin(9600);
  // when pin D2 goes high, call the rising function
  attachInterrupt(1, rising, RISING);
}
 
void loop() { 
  
  }
 
void rising() {
  attachInterrupt(1, falling, FALLING);
  prev_time = micros();
}
 
void falling() {
  attachInterrupt(1, rising, RISING);
  pwm_value = micros()-prev_time;
  Serial.println(pwm_value);
}
