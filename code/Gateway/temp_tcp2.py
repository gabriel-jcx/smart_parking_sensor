#!/usr/bin/env python
import datetime
import socket
import sys
#sys.path.insert(0, '/home/pi/cmpe123/code/Cloud/Structure1-0/')
import thread
import Cloud_APIs as gcloud_demo
import vision
#import decoder as vision
import time
TCP_IP = ''
TCP_PORT = 6001
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response
PARKING_LOT = "East-Remote"
lot_name = "eastRemote"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
while(1):
      try:
         s.listen(2)
         conn, addr = s.accept()
         print 'Connection address:', addr
         while 1:
            try:
               data = conn.recv(BUFFER_SIZE)
               if not data: break
               print "Recieved: " + data
               data_p = data.split(',')
               image_name = data_p[0]+'_test.jpg'
               if(data_p[1] == 'StatusChanged'):
                  if(data_p[2] == 'empty'):
                     #log spot as empty
                     #vision.log("log-uploadviagateway",data_p[0],data_p[2],"NULL")
                     print data_p[0]
                     gcloud_demo.free_space(data_p[0])
                     conn.send('#A') #send ack
                     print "Sent Auth, space empty"
                  else:
                     conn.send('#P')
                     print "req picture from ESP32"
                     f = open(image_name,'wb')
                     data = conn.recv(1024)
                     while data:
                        f.write(data)
                        data = conn.recv(1024)
                     f.close()
                  print("Finished Downloading test.jpg")
               if(data_p[1] == 'AnyTasks'):
                  print "no tasks for esp32"
                  conn.send('#T') #send ack
               if(data_p[1] == 'Picture'):
                  with open('test.bmp', 'wb') as f:
                     print "Opened test.bmp"
                     while True:
                        data = conn.recv(BUFFER_SIZE)
                        if not data:
                           f.close();
                           print "file closed"
                           break
                        f.write(data)
               if(data_p[1] == 'Auth'):
                  if(len(data_p) >= 2):
                     print "status changed to " + data_p[2]
                     user_code = vision.get_code(image_name)
                     #vision.log("log-uploadviagateway",data_p[0],data_p[2],user_code)
                     #log in the storage no longer needed
                     print "User {}, is trying to claim {}".format(user_code, data_p[0])
                     vision.upload_blob("images-uploadviagateway",image_name,lot_name+"_"+data_p[0] + "_image.jpg")
                     if(gcloud_demo.claim_space(data_p[0],user_code) == 0):
                        conn.send('#A') #send ack
                        print "Sent Auth"
                     else:
                        conn.send('#D') #send deny
                        print "Sent Deny"
            except socket.error:
               print socket.error
               print "The socket erorr occurred"
               pass
      except KeyboardInterrupt:
         print "Ctrl+C pressed"
         s.close()
         time.sleep(1)
         sys.exit(1)
