#!/bin/bash

# Advertising flags
AD_FLAGS="02 01 06"

# Beacon protocol. All items prefilled here cannot be edited, those which can are taken from the profile
AD_LENGTH="03"
AD_TYPE="03"
MFG_ID="AA FE"
BEACON_CODE="0b 16"
#                       h  e  l  l  o                 w  o  r  l  d
BEACON_ID="aa fe 00 00 68 65 6c 6c 6f 00 00 00 00 00 77 6f 72 6c 64 00"
REFERENCE_RSSI="00"
MFG_RESERVED="00"

Ad_Flags=`echo "$AD_FLAGS"`
Advertisement=`echo "$AD_LENGTH $AD_TYPE $MFG_ID $BEACON_CODE $BEACON_ID $REFERENCE_RSSI $MFG_RESERVED"`

# Commands running on Raspberry Pi
BLE="hci0"

# Turn off BLE
sudo hciconfig $BLE down

# Turn on BLE
sudo hciconfig $BLE up

# Stop LE advertising
sudo hciconfig $BLUETOOTH_DEVICE noleadv

# Start LE advertising (non-connectable)
sudo hciconfig $BLE leadv 3

# Turn scanning off (can sometimes affect advertising)
sudo hciconfig $BLE noscan

# Set the Beacon
sudo hcitool -i $BLE cmd 0x08 0x0008 13 $Ad_Flags $Advertisement
