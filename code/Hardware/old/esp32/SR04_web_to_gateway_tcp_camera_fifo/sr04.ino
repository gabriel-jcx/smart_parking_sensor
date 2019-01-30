
#define TRIG_DIS 60 //cm

char spotStatus() {
  long distance = (SR04() + SR04() + SR04() + SR04() )/4; //AVG of the two distance
  //#ifdef DEBUG
    Serial.printf("SR04 distance: %d cm\n", distance);
  //#endif
  if(distance < TRIG_DIS){
    return 0xFF;
  } else {
    return 0x00;
  }
}

long SR04(){
  digitalWrite(TRIGGER, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIGGER, HIGH);
  delayMicroseconds(10);

  digitalWrite(TRIGGER, LOW);
  duration = pulseIn(ECHO, HIGH);
  return (duration/2) / 29.1;
  delay(10);
}
