
#define TRIG_DIS 20 //cm

char spotStatus() {
  long distance = (SR04() + SR04() )/2; //AVG of the two distance
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
}
