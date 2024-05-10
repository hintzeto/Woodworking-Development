import socket
import json
import os

INVENTORY_FILE = "C:\\Woodworking\\Development\\Woodworking-Development\\Networking\\inventory.json"

# Initialize inventory or load from the file
if os.path.exists(INVENTORY_FILE):
    try:
        with open(INVENTORY_FILE, 'r') as file:
            inventory = json.load(file)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading inventory file: {e}")
        inventory = {}
else:
    inventory = {}

# Function to save the inventory
def save_inventory():
    with open(INVENTORY_FILE, 'w') as file:
        json.dump(inventory, file, indent=4)

# Initialize server socket
serversocket = socket.socket()
print("Socket successfully created")

port = 38204

# Bind the socket
serversocket.bind(('', port))
print(f"socket binded to {port}")

# Put the socket into listening mode
serversocket.listen(5)
print("socket is listening")

# Start accepting clients
try:
    while True:
        client, address = serversocket.accept()
        print('Got connection from', address)

        client.send(b'Thank you for connecting\n')

        data = client.recv(1024).strip()
        if not data.isdigit():
            client.send(b"Invalid option\n")
            client.close()
            continue

        option = int(data)
        print(f"Received option: {option}")

        if option == 1:
            for item, value in inventory.items():
                to_send = f"{item}: {value}\n"
                client.send(bytes(to_send, "utf-8"))
                print(f"{item} sent")
            client.send(b"stop\n")
            print("Sent stop")

        elif option == 2:
            item = client.recv(1024).decode("utf-8").strip()
            qty = int(client.recv(1024).strip())

            # Update the inventory
            if item in inventory and isinstance(inventory[item], dict):
                subitem = client.recv(1024).decode("utf-8").strip()
                inventory[item][subitem] = qty
                print(f"Updated {item} ({subitem}): {qty}")
            else:
                inventory[item] = qty
                print(f"Updated {item}: {qty}")

            save_inventory()
            client.send(b"Inventory updated\n")
        else:
            client.send(b"Invalid option\n")
            print("Invalid option sent")

except (ValueError, KeyError) as e:
    print(f"Error processing client request: {e}")
    client.send(b"Error processing request\n")

finally:
    serversocket.close()
    print("Socket closed")
