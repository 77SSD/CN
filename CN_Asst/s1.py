import socket
import threading

def handle_client(client_socket, clients_info, client_name):
    try:
        # Prompt client for their name
        client_socket.sendall(b"Enter your name: ")
        name = client_socket.recv(1024).decode().strip()

        # Prompt client for their public key
        client_socket.sendall(b"Enter the public key: ")
        public_key = client_socket.recv(1024).decode().strip()

        # Store client's name and public key in the dictionary
        clients_info[name] = public_key

        # Broadcast the new client's information to all connected clients
        broadcast_clients_info(client_socket, clients_info)

        # Print the received data
        print(f"Name: {name}, Public Key: {public_key}")

        # Print the dictionary of clients' information
        print("Clients Info:", clients_info)

        # Receive and broadcast encrypted messages
        while True:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                break
            broadcast_encrypted_message(client_socket, clients_info, encrypted_message, client_name)

    except Exception as e:
        print("Error:", e)

    finally:
        # Close the connection
        client_socket.close()

def broadcast_clients_info(client_socket, clients_info):
    broadcast_msg = str(clients_info)
    for client in clients_info:
        client_socket.sendall(broadcast_msg.encode())

def broadcast_encrypted_message(client_socket, clients_info, encrypted_message, client_name):
    for name, public_key in clients_info.items():
        # Skip broadcasting to the client who sent the message
        if name != client_name:
            client_socket.sendall(encrypted_message)

def main():
    # Define host and port
    host = '0.0.0.0'  # Use '0.0.0.0' to accept connections from any interface
    port = 5000  # Choose a port number

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the host and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(5)  # Allow up to 5 queued connections

    print("Server is listening for incoming connections...")

    clients_info = {}  # Dictionary to store clients' information

    while True:
        # Accept connection from client
        client_socket, client_address = server_socket.accept()
        print("Connection established with", client_address)

        # Handle client in a separate thread
        client_thread = threading.Thread(target=handle_client, args=(client_socket, clients_info, client_address[0]))
        client_thread.start()

if __name__ == "__main__":
    main()
