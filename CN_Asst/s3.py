import socket
import threading
import os

# Dictionary to store client name and public key
clients = {}

# Server directory containing video files of different resolutions
VIDEO_DIR = "videos/"

def handle_client(client_socket, addr):
    global clients

    # Receive client's name and public key
    client_name = client_socket.recv(1024).decode()
    public_key = client_socket.recv(1024).decode()

    # Store client's name and public key
    clients[client_name] = public_key

    # Broadcast updated dictionary to all clients
    broadcast_clients()

    try:
        while True:
            # Receive data from client
            data = client_socket.recv(1024)
            if not data:
                break

            # Handle client requests here

    except:
        # Handle client disconnection
        del clients[client_name]
        client_socket.close()
        broadcast_clients()

def broadcast_clients():
    global clients
    client_info = str(clients)
    for client_socket in clients.values():
        client_socket.send(client_info.encode())

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("Server started")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr} established.")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

if __name__ == "__main__":
    main()
