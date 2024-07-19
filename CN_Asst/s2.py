import socket
import threading
import pickle

# Dictionary to store client information
client_dictionary = {}

# Function to handle client connections
def handle_client(client_socket, client_address):
    global client_dictionary
    
    # Receive client name and public key
    client_name = client_socket.recv(1024).decode()
    public_key = client_socket.recv(4096)
    
    # Update dictionary with client information
    client_dictionary[client_name] = {'public_key': public_key}
    
    # Broadcast updated dictionary to all clients
    broadcast_dictionary()
    
    print(f"New client connected: {client_name} at {client_address}")
    print("Current Dictionary:", client_dictionary)
    
    # Handle client's requests (not implemented in this example)
    
    # Close client socket
    client_socket.close()

# Function to broadcast dictionary to all connected clients
def broadcast_dictionary():
    global client_dictionary
    data = {'clients': client_dictionary}
    for client_socket in client_sockets:
        client_socket.send(pickle.dumps(data))

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('localhost',5000)  # Change 'localhost' to the server's IP address if necessary
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(5)
print("Server is listening for connections...")

# List to store client sockets
client_sockets = []

try:
    while True:
        # Accept a new connection
        client_socket, client_address = server_socket.accept()
        
        # Add client socket to the list
        client_sockets.append(client_socket)
        
        # Create a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()
except KeyboardInterrupt:
    print("Server shutting down...")
finally:
    # Close all client sockets
    for client_socket in client_sockets:
        client_socket.close()
    
    # Close the server socket
    server_socket.close()
