import socket
import time
import  ssl
print("Hello World!")

host = ''
port = 6001

spot_amount = 1

#create context and load certificate
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

#initalize socket type to ipv4 and TCP
bs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created.")

#bind socket to exsisting host and port and error checking
try:
   bs.bind((host, port))
except socket.error as msg:
    print(msg)
print("Socket bind complete.")

#listen for spot_amount connections
bs.listen(spot_amount)

#accepts the incoming connection for each client and returns the connection descriptor and the clients address
conn, address = bs.accept()
print("accpeted")
s = context.wrap_socket(conn, server_side=True) 
print("Connected to: " + address[0] + ":" + str(address[1]))
#s.setblocking(True)

# while(1):
# 	time.sleep(.0001)
# 	hi = 1



data = s.recv(1024)

print (data.decode())

s.send(data)

s.close()
