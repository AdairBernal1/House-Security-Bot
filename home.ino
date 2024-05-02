#include <Wire.h>

#define echoPin1 2
#define trigPin1 4
#define echoPin2 18 // Nuevo sensor
#define trigPin2 5 // Nuevo sensor
#define echoPin3 21 // Nuevo sensor
#define trigPin3 19 // Nuevo sensor

long duration1, distance1;
long duration2, distance2; // Nuevo sensor
long duration3, distance3; // Nuevo sensor

void setup(){
  Serial.begin (9600);
  pinMode(trigPin1, OUTPUT);
  pinMode(echoPin1, INPUT);
  pinMode(trigPin2, OUTPUT); // Nuevo sensor
  pinMode(echoPin2, INPUT);  // Nuevo sensor
  pinMode(trigPin3, OUTPUT); // Nuevo sensor
  pinMode(echoPin3, INPUT);  // Nuevo sensor
}

void loop(){
  // Sensor 1
  digitalWrite(trigPin1, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin1, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin1, LOW);
  duration1 = pulseIn(echoPin1, HIGH);
  distance1 = duration1 / 58.2;
  String disp1 = String(distance1);


  // Sensor 2
  digitalWrite(trigPin2, LOW); // Nuevo sensor
  delayMicroseconds(2);
  digitalWrite(trigPin2, HIGH); // Nuevo sensor
  delayMicroseconds(10);
  digitalWrite(trigPin2, LOW); // Nuevo sensor
  duration2 = pulseIn(echoPin2, HIGH); // Nuevo sensor
  distance2 = duration2 / 58.2; // Nuevo sensor
  String disp2 = String(distance2); // Nuevo sensor


  // Sensor 3
  digitalWrite(trigPin3, LOW); // Nuevo sensor
  delayMicroseconds(2);
  digitalWrite(trigPin3, HIGH); // Nuevo sensor
  delayMicroseconds(10);
  digitalWrite(trigPin3, LOW); // Nuevo sensor
  duration3 = pulseIn(echoPin3, HIGH); // Nuevo sensor
  distance3 = duration3 / 58.2; // Nuevo sensor
  String disp3 = String(distance3); // Nuevo sensor
  
  Serial.println(disp1 + "," + disp2 + "," + disp3); // Nuevo sensor

  delay(5000);
}
