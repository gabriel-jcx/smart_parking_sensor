#!/usr/bin/env python
import datetime
import socket
import sys
import errno
import threading
import thread
sys.path.insert(0, '/home/pi/cmpe123/code/Cloud/Structure1-0/Cloud_APIs')
import Cloud_APIs as gcloud_demo
#import ../Cloud/Structure1-0/Cloud_APIs as gcloud_demo
import vision
#import decoder as vision
import time

#****Constants and global variables****#
host = ''
port = 6001
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response
#PARKING_LOT = "East-Remote"
PARKING_LOT = ""
lot_name = "eastRemote"
SPOT_AMOUNT = 20
maxconnections = 1
pic_sema = threading.BoundedSemaphore(value=maxconnections)
gcloud_sema = threading.BoundedSemaphore(value=maxconnections)
blob_sema = threading.BoundedSemaphore(value=maxconnections)
vision_sema =  threading.BoundedSemaphore(value=maxconnections)
retries_sema =  threading.BoundedSemaphore(value=maxconnections)

retries = []

#*******Functions*******#

# initialzes server socket as ipv4 and TCP, binds it to exsisting host
# and specified port and listens for SPOT_AMOUNT connections.
def SetupServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host, port))
    except socket.error as msg:
        print(msg)
    print("Socket created and binded.")
    s.listen(SPOT_AMOUNT)
    return s

# accpets each incoming connection and returns connection descriptor
# and address.
def SetupConnection(s):
    conn, address = s.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))
    return conn, address

# sends photo request and receives photo, writing it into a file.
def sendPic(con,name, spot_id):
  pic_sema.acquire()
  print ("Sent #P, Requesting photo from spot ", spot_id)
  con.send('#P')
  print ("req picture from ESP32")
  f = open(name,'wb')
  data = con.recv(1024)
  while data:
     f.write(data)
     data = con.recv(1024)
  f.close()
  pic_sema.release()

#parses message into various paramaters and returns them all.
def parseMessage(data):
  print ("Recieved: ", data)
  data_p      = data.split(',')
  temp_MAC    = data_p[0]
  #spot_id     = '2'
  lot_id      = gcloud_demo.MAC_map_to_spot(temp_MAC)
  temp_lot_id = lot_id.split(':')
  PARKING_LOT = temp_lot_id[0]
  spot_id     = temp_lot_id[1]
  print ("Parking lot is: {}".format(PARKING_LOT))
  print ("The spot id is: {}".format(spot_id))
  task_id     = data_p[1]
  spot_status = data_p[2]
  image_name  = 'spot_' + spot_id+ '_image.jpg'
  return conn, data_p, spot_id, task_id, spot_status, image_name

#Handles the exchange of data betwen sensor tower and cloud.
def SensorToCloud(conn, address, retries):

      #while (1):
        try:
           #Receive and parse data from sensor tower.
           data = conn.recv(BUFFER_SIZE)
           conn, data_p, spot_id, task_id, spot_status, image_name = parseMessage(data)

           #recovers retry value for each sensor tower. If it doesn't exsist, append onto list of retries.
           retry = -1
           retries_sema.acquire()
           for tup in retries:
              if spot_id in tup:
                 spot_id, retry = tup
                 break
           if(retry == -1):
              retry = 0
              retries.append((spot_id,retry))
           retries_sema.release()
           print ("The image name is: {}".format(image_name))

           #Excutes task based on data received from sensor box.
           if(task_id == 'StatusChanged'):

              #If spot status is empty, free space in cloud and send acknoledgement to sensor tower.
              if(spot_status == 'empty'):
                 print ("Sent #A, Freeing spot ", spot_id, " in the cloud")
                 gcloud_sema.acquire()
                 gcloud_demo.free_space(spot_id)
                 gcloud_sema.release()
                 conn.send('#A')
                 print ("Sent Auth, space empty\n\n")
                 retry = 0

              #Otherwise, it's taken and it requests photo from sensor box.
              else:
                 retry = 0 #reset retry
                 sendPic(conn,image_name,spot_id)
                 print("Finished Downloading image")

           #If received AnyTasks message, send acknoledgment to sensor box.
           if(task_id == 'AnyTasks'):
              print ("Sent #T, no tasks for esp32\n\n")
              conn.send('#T')
              retry = 0

           #If received 'Auth', run vision.get_code() method on image file.
           if(task_id == 'Auth'):
              print ("Reading QR code from spot " + spot_status)
              print ("Getting the QR code from the image: {}".format(image_name))
              vision_sema.acquire()
              user_code = vision.get_code(image_name)
              vision_sema.release()
              print spot_id + " has user code" + user_code

              #If an error occured reading photo, request another photo (up to 6 times).
              print spot_id + " retry is: " +  str(retry)
              if(user_code.startswith("ERROR") and retry < 6):
                 print ("ERROR: bad image decode, requesting new photo")
                 sendPic(conn,image_name, spot_id)
                 retry = retry + 1

              #Otherwise, upload image to blob and attempt to authorize user.
              else:
                 print ("User {}, is trying to claim {}".format(user_code, spot_id))
                 blob_sema.acquire()
                 vision.upload_blob("images-uploadviagateway",image_name,lot_name+"_" + spot_id + "_image.jpg")
                 blob_sema.release()
                 gcloud_sema.acquire()
                 authorization = gcloud_demo.claim_space(spot_id,user_code)
                 gcloud_sema.release()

                 #If authorized, send an authorized acknoledgement to sensor tower.
                 if(authorization == 0):
                    conn.send('#A') #send ack
                    print ("Sent #A, Turn on green LED\n\n")

                 #Otherwise send a denial acknoledgment to sensor tower.
                 else:
                    print ("finished")
                    conn.send('#D') #send deny
                 retry = 0

        except socket.error:
           print (socket.error)
           print (errno)
           print ("The socket erorr occurred")
           pass

        #writes updated value to retries list.
        a = 0
        print("Trying to update retries")
        for tup in retries:
           if spot_id in tup:
              retries[a] = (spot_id, retry)
              a = 0
              break
           a = a + 1
       #break
        print("Exited thread.")

#****** MAIN ********#
s = SetupServer()

#checks for new connections, adding a new thread to handle each one.
while(True):
  try:
     conn, address = SetupConnection(s)
     #thread.start_new_thread(SensorToCloud,(conn, address, retries))
     threading.Thread(target=SensorToCloud, args=(conn, address, retries)).start()
  except KeyboardInterrupt:
     print ("Ctrl+C pressed")
     s.close()
     print("Socket Closed")
     time.sleep(1)
     sys.exit(1)
