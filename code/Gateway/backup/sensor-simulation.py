#!/usr/bin/env python

#*****Libraries*****#
from __future__ import print_function
import sys
import socket
import time
#import pyqrcode
import sys
import time
#from PIL import Image
import os
import thread
import threading

#*****Constants*****#
HOST_IP = '10.3.141.1'
HOST_PORT = 6001
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"
input_file = "input-paramaters" #change this to a commandline argument.

#*****Functions*****#

# eprint is used instead of print in order to printing to stderr
# for testing purposes. (to print eprints and stderr to error-output do:
# python sensor-simulation 2> error-output
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# Parses input file and returns spot_id, photo name, and
# delay for sensor simulation. Also returns the sensor count. 
def parseInput(input_file):
    not_implemented = True
    f = open(input_file, 'r')
    spot_id = []
    photo = []
    delay = []
    sensor_count = 0
    for line in f:
        sensor_count = sensor_count + 1
        line = line.rstrip('\n').split(' ')
        spot_id.append(line[0])
        photo.append(line[1])
        delay.append(line[2])
    return spot_id, photo, delay, sensor_count

# Takes spot in psuedo parking lot. 
def takeSpot(s, spot_id, photo):
    eprint("Trying to take spot ", spot_id)
    s.connect((HOST_IP, HOST_PORT))
    eprint("Connected.")
    s.send((spot_id + ",StatusChanged,taken"))
    data = s.recv(BUFFER_SIZE).decode()
    brk = False
    loop2 = False
    while(1):
        # print("sdfjsd")
        # s.connect((HOST_IP, HOST_PORT))
        # eprint("Connected.")
        # s.send((spot_id + ",StatusChanged,taken"))
        # brk = False
        #data = s.recv(BUFFER_SIZE).decode() #utf-8?
        
        # print(type(data))
        # for each in unicode(data,"utf-8"):
        #     print(each)
        if(loop2 == False):
            if(data == '#P'):
                eprint ("received photo request.")
                sendPhoto(s, photo)
            if(data == '#A'):
                print("Authenticated user at spot ", spot_id)
                brk = True
            if(data == '#D'):
                print("Denied user at spot ", spot_id)
                brk = True
            else:
                s.close()
            if(brk == True):
                break

        if(loop2 == True):
            if(data == '#P'):
                eprint ("received photo request.")
                sendPhoto(sm, photo)
            if(data == '#A'):
                print("Authenticated user at spot ", spot_id)
                brk = True
            if(data == '#D'):
                print("Denied user at spot ", spot_id)
                brk = True
            else:
                sm.close()
            if(brk == True):
                break

        loop2 = True
        sm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sm.connect((HOST_IP, HOST_PORT))
        sm.send((spot_id + ",Auth,taken"))
        data = sm.recv(BUFFER_SIZE).decode()


# Leaves spot in pseduo parking lot.
def leaveSpot(s, spot_id):
    not_implemented = True
    eprint("Trying to leave spot: %s\n" % spot_id)
    s.connect((HOST_IP, HOST_PORT))
    s.send((spot_id + ",StatusChanged,empty").encode())
    while(1):
        data = s.recv(BUFFER_SIZE)
        if(data == '#A'):
            print("Spot %s now empty." % spot_id)
            s.close()
            break

# Pings gateway. (setup every so often?)
def pingGateway():
    not_implemented = True

# Sends photo to gateway.
def sendPhoto(s, photo_name):
    f = open( photo_name,'rb')
    sz = os.path.getsize(photo_name)
    eprint("sz = ", sz)
    loops = sz/BUFFER_SIZE
    loops = int(loops)
    eprint("loops = ", loops)
    f = open( photo_name,'rb')
    sz = os.path.getsize(photo_name)
    i = 0;
    while (loops > i):
        #eprint ("Sending image...")
        l = f.read(BUFFER_SIZE)
        s.send(l)
        i = i + 1
    l = f.read(sz % BUFFER_SIZE)
    s.send(l)

    print("done")

# Simulates user parking into sensor by providing real life
# paramaters including spot_id, a photo, and a delay between
# arrvial and exit.
def sensorSimulation(spot_id, photo, delay):
    print("sdf")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    takeSpot(s, spot_id, photo)
    print("done")
    so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    time.sleep(float(delay))
    leaveSpot(so, spot_id)
    print("complete!")

#*****Main*****#

# Parses the input_file for input paramaters for each spot.
# It then creates a new thread for each sensor simulation.
i = 0
spot_id, photo, delay, sensor_count = parseInput(input_file)
eprint(sensor_count)
t = []
while(sensor_count > i):
    
    spot_id_val, photo_val, delay_val = (spot_id[i], photo[i], delay[i])
    print(spot_id_val, photo_val, delay_val)
    #thread.start_new_thread(sensorSimulation (spot_id_val, photo_val, delay_val))
    t.append(threading.Thread(target=sensorSimulation, args=(spot_id_val, photo_val, delay_val)).start())
    i = i + 1
threading.active_count()

t.at(0).join()
t.at(1).join()
