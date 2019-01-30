#!/usr/bin/env python

import socket
import sys
#sys.path.insert(0, '/home/pi/cmpe123/code/Cloud/Structure1-0/')
import thread
import gcloud_demo

TCP_IP = ''
TCP_PORT = 6001
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
while(1):
	s.listen(2)

	conn, addr = s.accept()
	print 'Connection address:', addr
        try:
	    while 1:
    		data = conn.recv(BUFFER_SIZE)
    		if not data: break
                print "Recieved: " + data
                data_p = data.split(',')
                if(data_p[1] == 'StatusChanged'):
                    if(len(data_p) >= 2):
                        print "status changed to " + data_p[2]
                        if(data_p[2] == 'taken'):
                            if(gcloud_demo.claim_space(data_p[0],1234)):
                            #if(addr[1] % 2 == 0 or data_p[2] == "empty"):
                                conn.send('#A') #send ack
                                print "Sent Auth"
                            else:
                                conn.send('#D') #send deny
                                print "Sent Deny"
                        else:
                            gcloud_demo.free_space(data_p[0])
                            conn.send('#A') #send ack
                            print "Sent Auth, space empty"
                if(data_p[1] == 'AnyTasks'):
                    print "no tasks for esp32"
                    conn.send('#T') #send ack
        except KeyboardInterrupt:
            pass
	conn.close()
