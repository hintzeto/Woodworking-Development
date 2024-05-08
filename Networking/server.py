import socket

inventory = {
    "Epoxy Tape": 1,
    "Shims": 6,
    "Epoxy mixing buckets": 12,
    "MICA powder": 1,
    "Titebond 3": 1,
    "Sandpaper": {
        "120 grit": 5,
        "180 grit": 5,
        "220 grit": 5,
        "320 grit": 15
    }
}

serversocket = socket.socket()
print ("Socket successfully created")
 

port = 38204
 

serversocket.bind(('', port))
print (f"socket binded to {port}")
 
# put the socket into listening mode
serversocket.listen(5)    
print ("socket is listening")
 
# a forever loop until we interrupt it or an error occurs
try:
    while True:
    
        # Establish connection with client.
        (client, address) = serversocket.accept()
        print ('Got connection from', address )
    
        # send a thank you message to the client.
        client.send(b'Thank you for connecting')

        data = client.recv(1024)
        print(data)

        if data == b"y":
            for item in inventory:
                to_send = f"{item}: {inventory[item]}"
                client.send(bytes(to_send, "utf-8"))
                print(f"{item} sent")
            client.send(bytes("stop", "utf-8"))
        else:
            client.send(b"Inventory not requested")
            print("Inventory not sent")

finally:
    serversocket.close()