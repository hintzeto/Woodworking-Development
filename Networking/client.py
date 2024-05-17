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
    try:
        answer = int(input("1. print inventory\n2. Add Inventory\n3. something else\n-------------\nEnter Option: "))
        s.send(bytes(str(answer), "utf-8"))

        if answer == 1:

            inventory = []

            while True:
                received = s.recv(1024).decode("utf-8").strip()

                if received == 'stop':
                    break
                else:
                    inventory.append(received)

            print("\nInventory List:")
            for item in inventory:
                print(item)
            print("-------------")

        elif answer == 2:
            item = input("What item are you adding?")
            qty = input("How many of that item are you adding?")

            s.send(bytes(item, "utf-8"))
            s.send(bytes(qty, "utf-8"))
            print(f"Sent {item}: {qty} to inventory")

        elif answer == 0:
            break

        else:
            print("Invalid option. Please try again.")

    except ValueError:
        print("Invalid input. Please enter a valid number.")
    
 
# close the connection
s.close()

