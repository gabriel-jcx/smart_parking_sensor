#!/usr/bin/env python

import socket
import time

import pyqrcode
import sys
import time
from PIL import Image

TCP_IP = '10.3.141.1'
TCP_PORT = 6001
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect((TCP_IP, TCP_PORT))

def generate_qrcode(input_string,out_filename):
   code = pyqrcode.create(input_string)
   code.png(out_filename, scale = 6)
   im = Image.open(out_filename)
   rgb_im = im.convert('RGB')
   rgb_im.save(out_filename)



def takeSpaceQR(user_id, spot_id):
    print("takeSpaceQR")
    s.connect((TCP_IP, TCP_PORT))
    print("connected to port")
    message = spot_id + ",StatusChanged,taken"
    s.send(message)
    exit = 0
    while (exit == 0):
        rev_data = s.recv(BUFFER_SIZE)
        if(rev_data == '#P'):
            print("Got #P")
            generate_qrcode(user_id,user_id + ".jpg")
            f = open(user_id + ".jpg",'rb')
            l = f.read(BUFFER_SIZE)
            while (l):
                print "Sending image..."
                s.send(l)
                l = f.read(BUFFER_SIZE)
            #send picture data
            s.close()
            time.sleep(1)
            ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ss.connect((TCP_IP, TCP_PORT))
            ss.send(spot_id + ",Auth,taken")
            while(1):
                rev_data = ss.recv(BUFFER_SIZE)
                if(rev_data == '#A'):
                    print("User: %s is auth" % user_id)
                    ss.close()
                    exit = 1
                    break
                elif(rev_data == '#D'):
                    print("User: %s is deny")
                    ss.close()
                    exit = 1
                    break
        else:
            s.send(message)

def getAuth():
    s.connect((TCP_IP, TCP_PORT))
    s.send(spot_id + ",Auth,taken")
    while(1):
        rev_data = s.recv(BUFFER_SIZE)
        if(rev_data == '#A'):
            print("User: %s is auth" % user_id)
            s.close()
            break
        elif(rev_data == '#D'):
            print("User: %s is deny")
            s.close()
            break

#def takeSpaceAPP(user_id, spot_id):

def leaveSpot(spot_id):
    print("leaving spot: %s\n" % spot_id)
    s.connect((TCP_IP, TCP_PORT))
    message = spot_id + ",StatusChanged,empty"
    s.send(message)
    while (1):
        rev_data = s.recv(BUFFER_SIZE)
        if(rev_data == '#A'):
            print("Got ack, space: %s now empty" % spot_id)
            s.close()
            break

takeSpaceQR("1235","2")
#s.connect((TCP_IP, TCP_PORT))
#getAuth()
time.sleep(2)
leaveSpot("2")


#qr = pyqrcode.create(sys.argv[1])
#qr.png(sys.argv[2], scale=6)
#im = Image.open(sys.argv[2])
#rgb_im = im.convert('RGB')
#rgb_im.save(sys.argv[2])

