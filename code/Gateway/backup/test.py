
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
gcloud_sema = threading.BoundedSemaphore(value=maxconnections)
blob_sema = threading.BoundedSemaphore(value=maxconnections)
retries = []
vision.get_code(sys.argv[1])
