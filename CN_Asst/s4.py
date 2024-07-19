import socket
import pickle
import threading

# Global variables
clients = {}  # Dictionary to store client names and public keys
lock = threading.Lock()  # Lock to synchronize access to the clients dictionary
clients_sockets = []  # List to store client sockets
# Function to handle client connections
def handle_client(client_socket):
    while True:
        try:
            # Receive client name and public key
            client_name = client_socket.recv(1024).decode()
            serialized_public_key = client_socket.recv(4096)
            print(client_name , serialized_public_key)
            # Deserialize public key
            public_key = pickle.loads(serialized_public_key)
           

            # Add or update client details in the dictionary
            with lock:
                clients[client_name] = public_key
            print(clients)

            # Broadcast updated client details to all connected clients
            broadcast_client_details()

        except Exception as e:
            print(f"Error: {e}")
            break

    # If client disconnects, remove it from the dictionary and broadcast updated client details
    with lock:
        del clients[client_name]
    broadcast_client_details()

    # Close the client socket
    client_socket.close()

# Function to broadcast client details to all connected clients
def broadcast_client_details():
    for client_socket in clients_sockets:
        serialized_clients = pickle.dumps(clients)
        client_socket.send(serialized_clients)
    #print("Clients dictionary:", clients)  # Print the clients dictionary

# Create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
server_address = ('0.0.0.0', 1500)

# Bind the server socket to the address and port
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(50)  # Allow up to 50 queued connections

print("Server is listening for incoming connections...")

# clients_sockets = []  # List to store client sockets

while True:
    # Accept a new connection
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")

    # Append client socket to the list
    clients_sockets.append(client_socket)
    print("Clients dictionary:", clients)  # Print the clients dictionary
    # Create a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()

# Close the server socket
#server_socket.close()
