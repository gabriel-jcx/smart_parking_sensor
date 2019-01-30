
#ifdef BT
  
  
  void setBeacon() {
    char beacon_data[22];
    uint16_t beconUUID = 0xFEAA;
    uint16_t volt = 3300; // 3300mV = 3.3V
  
    Serial.printf(" Setting URL to https://%s\n",macAddr);//print 6 byte MAC address
    
    BLEAdvertisementData oAdvertisementData = BLEAdvertisementData();
    
    oAdvertisementData.setFlags(0x06); // GENERAL_DISC_MODE 0x02 | BR_EDR_NOT_SUPPORTED 0x04
    oAdvertisementData.setCompleteServices(BLEUUID(beconUUID));
  
      beacon_data[0]  = 0x10;  // Eddystone Frame Type (Eddystone-URL)
      beacon_data[1]  = 0x20;  // Beacons TX power at 0m
      beacon_data[2]  = 0x03;  // URL Scheme 'https://'
      beacon_data[3]  = macAddr[0]; //sets the MAC address as the URL
      beacon_data[4]  = macAddr[1];
      beacon_data[5]  = macAddr[2];
      beacon_data[6]  = macAddr[3];
      beacon_data[7]  = macAddr[4];
      beacon_data[8]  = macAddr[5];
      beacon_data[9]  = macAddr[6];
      beacon_data[10] = macAddr[7];
      beacon_data[11] = macAddr[8];
      beacon_data[12] = macAddr[9];
      beacon_data[13] = macAddr[10];
      beacon_data[14] = macAddr[11];

    #ifdef HARD_CODE_ADDR
      oAdvertisementData.setServiceData(BLEUUID(beconUUID), std::string(beacon_data, 4));
    #else
      oAdvertisementData.setServiceData(BLEUUID(beconUUID), std::string(beacon_data, 15));
    #endif
    
    pAdvertising->setScanResponseData(oAdvertisementData);
    delay(10);
    pAdvertising->start();
  
  }

#endif //BT
