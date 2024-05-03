import socket

# Create a socket object
s = socket.socket()
 
# Define the port on which you want to connect
port = 38204
####ip = input("Input your IP: ")
 
# connect to the server on local computer
s.connect(('127.0.0.1', port))
 
# receive data from the server
print(s.recv(1024))

s.send(bytes(input("Do you want to get invetory information? (y/n)").lower(), "utf-8"))

loop_count = int.from_bytes(s.recv(4096), "little")

for i in range(loop_count):
    received = s.recv(1024)
    print(received)
    
 
# close the connection
s.close()

