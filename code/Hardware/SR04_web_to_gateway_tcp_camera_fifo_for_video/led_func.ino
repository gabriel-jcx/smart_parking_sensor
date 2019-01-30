// Fill the dots one after the other with a color
void colorWipe(uint32_t c, uint8_t wait) {
  for(uint16_t i=0; i<strip.numPixels(); i++) {
    strip.setPixelColor(i, c);
    strip.show();
    delay(wait);
  }
}

void colorWipeGreen( uint8_t wait) {
  for(uint16_t i=0; i<strip.numPixels(); i++) {
    strip.setPixelColor(i, strip.Color(255, 0,0));
    strip.show();
    delay(wait);
  }
}

void colorWipeRed( uint8_t wait) {
  for(uint16_t i=0; i<strip.numPixels(); i++) {
    strip.setPixelColor(i, strip.Color(0, 255,0));
    strip.show();
    delay(wait);
  }
}

// Fill the dots one after the other with a color
void colorWipeUCSC( uint8_t wait) {
  for(uint16_t i=0; i<strip.numPixels(); i++) {
    if((i % 10) < 5){ 
      strip.setPixelColor(i, strip.Color(30, 0, 255));
    } else {
      strip.setPixelColor(i, strip.Color(199, 253, 0));
    }
    strip.show();
    delay(wait);
  }
}



//Theatre-style crawling lights.
void theaterChase(uint32_t c, uint8_t wait) {
  for (int j=0; j<10; j++) {  //do 10 cycles of chasing
    for (int q=0; q < 5; q++) {
      for (uint16_t i=0; i < strip.numPixels(); i=i+5) {
        strip.setPixelColor(i+q, c);    //turn every third pixel on
      }
      strip.show();

      delay(wait);

      for (uint16_t i=0; i < strip.numPixels(); i=i+5) {
        strip.setPixelColor(i+q, 0);        //turn every third pixel off
      }
    }
  }
}
