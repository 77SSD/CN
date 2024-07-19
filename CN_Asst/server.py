import socket
import threading
import base64
import pickle
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Define server address and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000

# Initialize client dictionary
clients = {}

# Function to handle client connections
def handle_client(client_socket, address):
    print(f"[*] Accepted connection from {address}")

    try:
        # Receive client's name and public key
        name = client_socket.recv(1024).decode().strip()
        public_key = client_socket.recv(2048)

        # Store client's name and public key
        clients[name] = public_key

        # Broadcast client's name and public key to all connected clients
        broadcast(f"{name}:{public_key}".encode())

        # Main loop for client communication
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            # Check if the client requests the client dictionary
            if data.decode().strip() == "GET_CLIENT_DICT":
                try:
                    serialized_client_dict = pickle.dumps(clients)
                    client_socket.send(serialized_client_dict)
                    print("Sent client dictionary to client:", clients)  # Debug print
                except Exception as e:
                    print(f"Error sending client dictionary: {e}")
            else:
                # Proceed with other message processing
                # Decrypt message, handle QUIT command, etc.
                pass

    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        print(f"[*] Closing connection with {address}")
        client_socket.close()
        del clients[name]

# Function to broadcast a message to all connected clients
def broadcast(message):
    for client_socket in clients_sockets:
        try:
            client_socket.send(message)
        except Exception as e:
            print(f"Error broadcasting message: {e}")
            client_socket.close()
            clients_sockets.remove(client_socket)

# Create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the server socket to the address and port
server_socket.bind((SERVER_HOST, SERVER_PORT))

# Listen for incoming connections
server_socket.listen(5)
print(f"[*] Listening on {SERVER_HOST}:{SERVER_PORT}")

# List to store client sockets
clients_sockets = []

try:
    while True:
        # Accept incoming connection
        client_socket, address = server_socket.accept()

        # Append client socket to the list
        clients_sockets.append(client_socket)

        # Handle client in a separate thread
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

except KeyboardInterrupt:
    print("[*] Server shutting down.")
    for client_socket in clients_sockets:
        client_socket.close()
    server_socket.close()
