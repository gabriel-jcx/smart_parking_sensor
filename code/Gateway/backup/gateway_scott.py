#!/usr/bin/env python
import datetime
import socket
import sys
sys.path.insert(0, '/home/pi/cmpe123/code/Cloud/Structure1-0/Cloud_APIs')
import thread
import Cloud_APIs as gcloud_demo
#import ../Cloud/Structure1-0/Cloud_APIs as gcloud_demo
import vision
#import decoder as vision
import time

import binascii

TCP_IP = ''
TCP_PORT = 6001
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response
PARKING_LOT = "East-Remote"
lot_name = "eastRemote"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))

def ByteToHex( byteStr ):
    """
    Convert a byte string to it's hex string representation e.g. for output.
    """

    # Uses list comprehension which is a fractionally faster implementation than
    # the alternative, more readable, implementation below
    #
    #    hex = []
    #    for aChar in byteStr:
    #        hex.append( "%02X " % ord( aChar ) )
    #
    #    return ''.join( hex ).strip()

    return ''.join( [ "%02X " % ord( x ) for x in byteStr ] ).strip()

def sendPic(con,name):
  print "Sent #P, Requesting photo from spot " + spot_id
  con.send('#P')
  print "req picture from ESP32"
  f = open(name,'wb')
  data = con.recv(1024)
  while len(data) != 0:
     f.write(data)
     data = con.recv(1024)
     #print(len(data))
     if(len(data) != 0):
#         print ''.join('{:02x}'.format(x) for x in data)
#         print ''.join('{:02x}'.format(data[len(data)-2])
#         print ''.join('{:02x}'.format(data[len(data)-1])
         print(ByteToHex(data[len(data)-2]), ByteToHex(data[len(data)-1]))
         #print(ByteToHex(data[len(data)-1]))
         if(ByteToHex(data[len(data)-2]) == 'FF' and ByteToHex(data[len(data)-1]) == 'D9'):
             print("EOF")
  f.close()
  time.sleep(0.01)


retry = 0
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

               #Read the data from the sensor box
               data_p      = data.split(',')
               #spot_id     = data_p[0]
               spot_id     = '2'
               task_id     = data_p[1]
               spot_status = data_p[2]
               image_name  = 'spot_' + spot_id+ '_image.jpg'

               #excute task
               if(task_id == 'StatusChanged'):
                  if(spot_status == 'empty'):
                     print "Sent #A, Freeing spot " + spot_id + " in the cloud"
                     gcloud_demo.free_space(spot_id)
                     conn.send('#A') #send ack
                     print "Sent Auth, space empty\n\n"
                  else:
                     retry = 0 #reset retry
                     sendPic(conn,image_name)
                     print("Finished Downloading image")
               if(task_id == 'AnyTasks'):
                  print "Sent #T, no tasks for esp32\n\n"
                  conn.send('#T') #send ack
               if(task_id == 'Auth'):
                  print "Reading QR code from spot " + spot_status
                  user_code = vision.get_code(image_name)
                  if(user_code.startswith("ERROR") and retry < 6):
                     print "ERROR: bad image decode, requesting new photo"
                     sendPic(conn,image_name)
                     retry = retry + 1
                  else:
                     print "User {}, is trying to claim {}".format(user_code, spot_id)
                     vision.upload_blob("images-uploadviagateway",image_name,lot_name+"_" + spot_id + "_image.jpg")
                     if(gcloud_demo.claim_space(spot_id,user_code) == 0):
                        conn.send('#A') #send ack
                        print "Sent #A, Turn on green LED\n\n"
                     else:
                        if(retry < 6):
                           retry = retry + 1
                           sendPic(conn,image_name)
                        else:
                           conn.send('#D') #send deny
                           print "Sent #D, Turn on red LED\n\n"
            except socket.error:
               print socket.error
               print "The socket erorr occurred"
               pass
      except KeyboardInterrupt:
         print "Ctrl+C pressed"
         s.close()
         time.sleep(1)
         sys.exit(1)
