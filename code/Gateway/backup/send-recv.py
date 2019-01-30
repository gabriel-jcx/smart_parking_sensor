import socket
import time

print("Hello World!")

host = ''
port = 6001

spot_amount = 1

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
def SetupConnection(s): #!! why do I not need an arguemnet for s in here
    
    #accepts the incoming connection for each client and returns the connection descriptor and the clients address
    conn, address = s.accept() 
    print("Connected to: " + address[0] + ":" + str(address[1]))
    #s.setblocking(True)
    return conn, address

# while(1):
# 	time.sleep(.0001)
# 	hi = 1


s = SetupServer()
conn, address = SetupConnection(s)

data = conn.recv(1024)

print (data)

conn.send(data)

conn.close()
