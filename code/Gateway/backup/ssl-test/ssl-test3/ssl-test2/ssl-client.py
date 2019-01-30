import ssl
#from socket import *             # Imports socket module
import socket
#host = "127.168.2.75"
#host = "10.0.0.9"
host = "10.3.141.1"
port=6001            
print("sdfsdf") 
#context = ssl.create_default_context()
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ssl_sock = ssl.wrap_socket(s,
                           ca_certs= "server.crt")#,
#                           cert_reqs=ssl.CERT_REQUIRED,
#                           ssl_version=ssl.PROTOCOL_TLSv1)
#s = context.wrap_socket(socket(AF_INET),host)
#s = context.wrap_socket(socket(AF_INET, SOCK_STREAM))      # Creates a socket
print("socket created")
ssl_sock.connect((host,port))          # Connect to server address
print("connected")
ssl_sock.send(str.encode("hello ~MySSL !"))
#ssl_sock.send('y')           # Receives data upto 1024 bytes and stores in variables msg
print("sent")

 
ssl_sock.close()                            # Closes the socket 
# End of code
