import socket
from Crypto.PublicKey import RSA
import threading
import os

# Define server address and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5002
lock = threading.Lock()


# Dictionary to store client names and public keys
clients = {}  # Dictionary to store client names and public keys
clients_sock={}
# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Bind the socket to a specific address and port
server_socket.bind(('0.0.0.0', 5000))          # Listen for incoming connections
server_socket.listen(1)
print("Server is listening for incoming connections...")  

# Function to send video frames over the socket
def send_video(conn, video_files):
    frame_counts = [0] * len(video_files)
    current_file_index = 0
    while current_file_index < len(video_files):
        cap = cv2.VideoCapture(video_files[current_file_index])
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        start_frame = (total_frames // 3)*current_file_index
        end_frame = (total_frames // 3) * (current_file_index+1)
        print("start_frame: ", start_frame, " end_frame: ", end_frame, "total_frames: ", total_frames)
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            # Serialize frame
            frame_data = cv2.imencode('.jpg', frame)[1].tobytes()
            # Send frame size and data
            conn.sendall((str(len(frame_data))).encode().ljust(16) + frame_data)
            # Switch to the next file if one-third of frames sent
            if  current_frame >= end_frame:
                current_file_index += 1
                break

        cap.release()

def handle_client(client_socket, address):
    global clients
    print(f"[*] Accepted connection from {address}") # Accept a connection
#client_socket, address = server_socket.accept()
    print(f"Connection from {address} has been established.")
    client_data = client_socket.recv(1024).decode()
    print(client_data)
    #client_data = "client_name: public_key"  # Example string
    #if ": " in client_data:
        # parts = client_data.split(": ")
        # if len(parts) == 2:
    client_name, public_key = client_data.split(":")
    with lock:
        clients[client_name] = public_key
        clients_sock[client_name]=client_socket
        print(f"Stored {client_name}'s public key in the clients dictionary.")
        print(f"upadated_dir: {clients}")
        # Broadcast the updated clients dictionary to all connected clients
        broadcast_clients()

    # else:
    #     print("Invalid client data format")
    #     client_socket.send(b"Invalid client data format")
    #     client_socket.close()
    #     return

    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                break

            # Check if client wants to disconnect
            if data.strip().decode()== "QUIT":
                client_socket.send(b"Goodbye!")
                if client_name in clients:
                    del clients[client_name]
                    broadcast(f"{client_name} has left the chat.".encode())
                    # Broadcast the updated clients dictionary to all connected clients
                    broadcast_clients()
                break
            
            parts = data.strip().decode().split(":")
            if len(parts) == 2:
                recipient_name, message = parts
                if recipient_name in clients:
                    clients_sock[recipient_name].send(message)
                    # recipient_public_key = RSA.import_key(clients[recipient_name])
                    # cipher_rsa = PKCS1_OAEP.new(recipient_public_key)
                    # encrypted_message = cipher_rsa.encrypt(message.encode())
                    
            # else:
            #     print("Invalid message format")
            #     client_socket.send(b"Invalid message format")

    except Exception as e:
        print(f"Error: {e}")
        if client_name in clients:
         del clients[client_name]
        client_socket.close()

# Function to broadcast a message to all connected clients
def broadcast(message):
    for client_socket in clients_sockets:
        client_socket.send(message)

        # Function to broadcast updated clients dictionary to all connected clients
def broadcast_clients():
    clients_data = str(clients).encode()
    for client_socket in clients_sockets:
        client_socket.send(clients_data)

# Function to stream video frames
def stream_video(client_socket, video_name):
    # Stream frames proportionately from each resolution video file
    for resolution in VIDEO_RESOLUTIONS:
        video_file_path = os.path.join(VIDEO_DIRECTORY, f"{video_name}_{resolution}.mp4")
        with open(video_file_path, "rb") as f:
            while True:
                frame = f.read(1024)
                if not frame:
                    break
                client_socket.send(frame)

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
 
        # Receive requested video file name from client
        video_name = client_socket.recv(1024).decode()
        print(f"[*] Received request for video: {video_name}")

        try:
            # Generate video file names with different resolutions
            video_files = [
                f"{video_name}_240p.mp4",
                f"{video_name}_720p.mp4",
                f"{video_name}_1440p.mp4"
            ]
            # Send requested video
            send_video(conn, video_files)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Close connection
            client_socket.close()
except KeyboardInterrupt:
    print("[*] Server shutting down.")
    for client_socket in clients_sockets:
        client_socket.close()
    server_socket.close()
