import socket

# Create a socket object
s = socket.socket()
 
# Define the port on which you want to connect
port = 38204
 
# connect to the server on local computer
s.connect(('127.0.0.1', port))
 
# receive data from the server
print(s.recv(1024))

while True:
    answer = int(input("1. print inventory\n2. Add Inventory\n3. something else\n-------------\nEnter Option: "))

    if answer == 1:

        inventory = []

        while True:
            received = (s.recv(1024))

            if received == b'stop':
                break
            else:
                inventory.append(str(received, encoding="utf-8"))

        print(inventory)

    elif answer == 2:

    elif answer == 0:
        break
    
 
# close the connection
s.close()

