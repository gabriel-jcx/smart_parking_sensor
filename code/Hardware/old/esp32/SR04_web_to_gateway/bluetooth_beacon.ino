
#ifdef BT
  
  
  void setBeacon() {
    char beacon_data[22];
    uint16_t beconUUID = 0xFEAA;
    uint16_t volt = 3300; // 3300mV = 3.3V
  
    
    BLEAdvertisementData oAdvertisementData = BLEAdvertisementData();
    
    oAdvertisementData.setFlags(0x06); // GENERAL_DISC_MODE 0x02 | BR_EDR_NOT_SUPPORTED 0x04
    oAdvertisementData.setCompleteServices(BLEUUID(beconUUID));
  
      beacon_data[0] = 0x10;  // Eddystone Frame Type (Eddystone-URL)
      beacon_data[1] = 0x20;  // Beacons TX power at 0m
      beacon_data[2] = 0x03;  // URL Scheme 'https://'
      beacon_data[3] = 'u';  // URL add  1
      beacon_data[4] = 'c';  // URL add  2
      beacon_data[5] = 's';  // URL add  3
      beacon_data[6] = 'c';  // URL add  4
      beacon_data[7] = '.';  // URL add  5
      beacon_data[8] = 'e';  // URL add  6
      beacon_data[9] = 'd';  // URL add  7
      beacon_data[10] = 'u';  // URL add  8
      beacon_data[11] = '/';  // URL add  9
      beacon_data[12] = '1';  // URL add 10
      beacon_data[13] = '/';  // URL add 11
      beacon_data[14] = '2';  // URL add 12
      beacon_data[15] = '3';  // URL add 13
      beacon_data[16] = '3';  // URL add 14
    
    oAdvertisementData.setServiceData(BLEUUID(beconUUID), std::string(beacon_data, 17));
    
    pAdvertising->setScanResponseData(oAdvertisementData);
  
  }

#endif //BT
