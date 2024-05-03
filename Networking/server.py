import socket
import signal
import sys
import keyboard

def signal_handler(sig, frame):
    print('Shutting down the server...')
    global serversocket
    serversocket.close()  # Close the server socket
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

inventory = {
    "Epoxy Tape": 1,
    "Shims": 6,
    "Epoxy mixing buckets": 12,
    "MICA powder": 1,
    "Titebond 3": 1,
    "Sandpaper": {
        "120 grit": 5,
        "180 grit": 5,
        "220 grit": 5
    }
}

# next create a socket object
serversocket = socket.socket()
print ("Socket successfully created")
 
# reserve a port on your computer in our
# case it is 38204
port = 38204
 
# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
serversocket.bind(('', port))
print (f"socket binded to {port}")
 
# put the socket into listening mode
serversocket.listen(5)    
print ("socket is listening")
 
# a forever loop until we interrupt it or
# an error occurs
try:
    while True:
    
        # Establish connection with client.
        (client, address) = serversocket.accept()
        print ('Got connection from', address )
    
        # send a thank you message to the client.
        client.send(b'Thank you for connecting')

        data = client.recv(4096)
        print(data)

        if data == b"y":
            client.send(len(inventory).to_bytes(5, "little"))
            for item in inventory:
                to_send = f"{item}: {inventory[item]}"
                client.send(bytes(to_send, "utf-8"))
                print(f"{item} sent")
        else:
            client.send(b"Inventory not requested")
            print("Inventory not sent")

        if keyboard.read_key() == "q":
            break

finally:
    serversocket.close()