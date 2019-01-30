#************Key**************#

# "!!" means go back and change

#************I/O:**************#

#OUT OF DATE !!
#incoming data to gateway tower:
#hardware taken/not taken ack, wakeup signal ack, based on either hardware signal

#outgoing data from gateay tower:
#request for old photo,request for current photo, authentication ack display message

#************To Do:**************#

#1. set the print statements as only printing out in debug mode
#2. add semaphores to the queue
#3. figure out encryption and decryption
#************Notes:**************#

#1. for photo requests, just have the admin put field on teh data store that says photo request and on the gateway cloud apis just check that field and fufill the request if needed

#************Local Directory**************#

#cd  /Users/davidcaplin/Documents/school/CE123A-Engineering-Design-Project-I/personal-material/program/gateway/2-way-many-clients

#************Methods and Classes:**************#

#import modules
import gcloud_demo
#sys.path.insert(0, '/home/pi/cmpe123/code/Cloud/Structure1-0/')
import decoder
import socket
import thread
import Queue

#fixed varaibles
NOT_UPDATED = 2
High = 1
Low = 0

#dynamic varaibles
spot_amount = 20

#socket variables
host = ''
port = 6001

#setup the server soket 
def SetupServer():

    #initalize socket type to ipv4 and TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created.")

    #bind socket to exsisting host and port and error checking
    try:
        s.bind((host, port))
    except socket.error as msg:
        print(msg)
    print("Socket bind complete.")

    #listen for spot_amount connections and return the socket descriptor
    s.listen(spot_amount)
    return s

#sets up the connection by accepting each incoming connection on the LAN. Blocks until a connection is established.
def SetupConnection(): #!! why do I not need an arguemnet for s in here
    
    #accepts the incoming connection for each client and returns the connection descriptor and the clients address
    conn, address = s.accept() 
    print("Connected to: " + address[0] + ":" + str(address[1]))
    #s.setblocking(True)
    return conn, address

#forwards sensor tower data to buffer that will eventually send to cloud when its request reaches front of queue
def SenorTowerToBuffer(conn, SensorTower, cloud_queue): 
    
    #receive data from sensor tower. Blocks for now !!.
    data = conn.recv(1024)

    #set sleep flags high that must be low in order for the sensor tower to sleep
    sleep_flag_car_event = High
    sleep_flag_photo_request = High
    
    #parse data
    parsed_data = data.split(',')
    spot_id = int(parsed_data[0])
   
    event = parsed_data[1]

    #set some varaibles equal to the exsisting class struct
    SensorTower[spot_id].conn = conn
    SensorTower[spot_id].address = address
    SensorTower[spot_id].established = True

    #if an event occured, parse the 3rd bit of data to see the updated status and fufill tasks for the new status
    if event == 'StatusChanged': 
        status = parsed_data[2]

         #if status is now taken, prepare to receive photo, run computer vision algorithm and put claim space request into queue
        if status == 'taken': 
            print("taken")
            #extract photo and save onto hard drive
            #run computer vision
            #send photo to blob
            qr_code = 1234
            cloud_queue.put(spot_id, status, qr_code) # !! need semaphores around the buffer so only 1 at a time can push into it

        #if status is now empty put data into cloud queue to be later sent to the cloud
        if status == 'empty': 
             cloud_queue.put(spot_id, status, 0)# 1!
             print("empty")
    #if the admin have requested a photo, then send the notification to the sensor tower, receive the photo and send to blob
    if SensorTower[spot_id].cloud_photo_request == High:
        SensorTower[spot_id].cloud_photo_request = Low
        conn.send('#P') 
        conn.recv(1024) #!! change to receive entire message
        #send to blob
        sleep_flag_photo_request = Low
        print("photo request")
    #otherwise, just set the photo request sleep flag low
    else:
        sleep_flag_photo_request = Low
        print("no photo request")
    #after the above has completed, if the status is taken, check the cloud authentication status until its updated and forward the authentication information    
    if event == 'StatusChanged': 
    	status = parsed_data[2]
    	if status == 'taken':
        	#check the cloud authentication status until its updated and forward the authentication information, then once the send has completed, set the car event sleep flag low   
        	while True:
                #print("taken and waiting on cloud")
                if SensorTower[spot_id].cloud_auth_status != NOT_UPDATED:
                    print("got cloud auth, sending back to sensorB")
    				if(SensorTower[spot_id].cloud_auth_status == 1):
    			  		conn.send("#A")
    					print("#A")
    					conn.close()
    					print("disconnected")
    					return
                    if(SensorTower[spot_id].cloud_auth_status == 0):
                        conn.send("#D")
                        print("#D")
    					conn.close()
    					print("disconnected")
                        return
                    SensorTower[spot_id].cloud_auth_status = NOT_UPDATED
                    sleep_flag_car_event = Low
                    break
	if status == 'empty':
		print("stil not taken")
		sleep_flag_car_event = Low
                           
    #otherwise, just set the car event sleep flag low    
    else: 
         sleep_flag_car_event = Low
         print("no car event")

    #if the sleep flags are both low then send an ack back to let the sensor tower know it can sleep
    print(sleep_flag_car_event)
    print(sleep_flag_photo_request) 
    if sleep_flag_car_event == Low and sleep_flag_photo_request == Low:
        conn.send('#A')
	print("tell sensor tower to sleep")
        conn.close()
        print("disconnected")
#data from the buffers get pushed to the cloud once they get to the front of the queue
def BufferToCloud(cloud_queue, SensorTower):

    # checks if the cloud queue isnt empty and forwards the data at the top of the FIFO queue to the cloud 
    while True: 
        if not cloud_queue.empty: #blocks if it is empty
            spot_id, status, qr_code = cloud_queue.get()
            print("about to push to cloud")
            #if its taken, forward to cloud with cloud API ClaimSpace(), and set return to the cloud authentication status
            if status == 'taken':
		qr_code = 1234
                SensorTower[spot_id].cloud_auth_status = gcloud_demo.claim_space(spot_id,qr_code) # !! claim space in database from the specific spaceID and qrCode for authentication     
                print("pushed taken to  cloud")
            #if its empty, forward to cloud with cloud API FreeSpace()
            elif status == 'empty':
		cloud_demo.free_space(spot_id)
	       # SensorTower[spot_id].cloud_auth_status = 1
                print("pushed empty to cloud")

#takes requests from admin for things such as photo request or configuration setup
# def CloudToBuffers():
#   parse data
#   receive from admin
#     while True:
#         message = raw_input("cloud_to_sensor_tower_message: ")
#         # op_code = parse first byte
#         if op_code == CURRENT_PHOTO_REQUEST or CONFIG_OPTION: #change to spot ID and request type (current pic, pic from certain time)
#            # conn[spot_id].send(message)


class Tower(object):
    def __init__(self, conn = None, address = None, established = None, cloud_photo_request = None, cloud_auth_status = None):
        self.conn = conn
        self.address = address
        self.established = established
        self.cloud_photo_request = cloud_photo_request
        self.cloud_auth_status = cloud_auth_status

#************Main:**************#

#initializing list of sensor towers
SensorTower = []
i = 0
while(i < spot_amount):
    SensorTower.append(Tower("0", "0", 0, 0, 0))
    i = i + 1

#initializing cloud queue
cloud_queue = Queue.Queue()

#setting up the server socket
s = SetupServer()

#create a new thread for Buffer to Cloud function
thread.start_new_thread(BufferToCloud,(cloud_queue, SensorTower))

while True:

    #accept connection from each tower as it connects to the hotspot
    conn, address = SetupConnection()

    #sends sensor tower info to buffer which will then get forwarded to cloud when its first on the queue
    thread.start_new_thread(SenorTowerToBuffer,(conn, SensorTower, cloud_queue))




#x = 0
#SensorTower[spot_id].photo_request
#SensorTower[spot_id].auth_status

#conn[1], address1 = SetupConnection()
# pre make a bunch of these and there threads and clear them as needed
#setup a list of conn based on the spotID that gets received 
#so first do conn, address = SetupConnection()
#then do that thing to make a list of classes that contain the connection, established 
#boolean, and maybe some other stuff we'll have to see, and indexable by the spotID
#somehow we are going to have to clear it when its done with the connection
#conn[2], address2 = SetupConnection()
#thread.start_new_thread(ClientThreadRecv,(conn[1],spaceID))
#thread.start_new_thread(ClientThreadRecv,(conn[2],spaceID))

#things to do:
#figure out flow chart for sleeping stuff
#figure out threadpooling
#figure out sending data files
#figure out encryption and decryption
#figure out class type if needed


#if sleeping then dont receive or send anything until its done so for the gateway that means disconnect and dont receive anything
# if sleeping then only send something to cloud if you've already recieved it

#so i think the best solution is to make sure that if its sending or receiving, wait for that to finish and then sleep
#either that or sleep on a set schedule and make sure that it isnt sending or receiving

#CloudToSenorTowers()
#while True: #*N why is it double shifted?
#         # receiving cloud command
#         fromCloudMsg = raw_input("Enter your command ")
#         # opCode = parse first byte
#         if opCode == CURRENT_PHOTO_REQUEST or DISPLAY_AUTH_MESSAGE or DISPLAY_NOT_AUTH_MESSAGE or CONFIG_OPTION: #change to spot ID and request type (current pic, pic from certain time)
#             conn[spot_id].send(fromCloudMsg)
#         if command == "EXIT":
#             conn[1].send(command)
#             conn[2].send(command)
#             s.close()
#             break
#         else: 
#             print("incorrect input, try again")
# conn[1].close()
# conn[2].close()

# CONFIG.
# 1. towers will have tags with the predefined spot IDs on them that must be in 
#    order, or the physical screen will have an proccess at boot time that
#    allows config of spotID.
#
# REGULAR OPERATION
# 2. UDP discovery protocol will make sure they are all found and don't get 
#    discovered twice or a certain gateway is set to certain sensor towers
#    will there be a certain gateway is set to certain sensor towers or
#    1+ gateways arbitrating connection rights between sensor towers?*N 
#    well if its the latter, then there will be problems in regards to
#    the cloud knowing which gateways corespond to which towers. 
#    I guess you could ping for it on the network and find it that way    
#    
# 3. TCP connection will be invoked for all of the towers, however it should be
#    non blocking so that incase there is a issue with 1 of them, it doesn't
#    block the whole thing (*N when would there be an issue?)
#
# 4. set up recieving threads for all of the clients in a loop
#
# 5. while loop waiting for a signal from the cloud to send a request for a
#    a cached photo(s) or a current photo (forward to pi) 
# 
#
# what sort of data types do we need:
# well we have space and QR code going to the cloud deciphered by either freeing
# or claiming space
#
#
# take in GPIO signal
# get the list going for different threads
# get the picture stuff
# get the error checking
#get the cloud stuff
# get the file stuff
# possible locks required for camera 




