sudo hciconfig hci0 up
sudo hciconfig hci0 leadv 3
sudo hcitool -i hci0 cmd 0x08 0x0008 1f 02 01 06 03 03 aa fe 17 16 aa fe 10 00 03 75 63 73 63 02 35 2f 33 2f 32 35 35 35 35 35 35 35
sudo hcitool -i hci0 cmd 0x08 0x0008 1f 02 01 06 03 03 aa fe 17 16 aa fe 10 00 03 75 63 73 63 02 35 2f 33 2f 32 35 35 35 35 35 35 35
