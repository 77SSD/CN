import socket
import threading
import base64

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Define server address and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5002

# Dictionary to store client names and public keys
client_dict = {}

def receive_video(client_socket):
    while True:
        # Receive frame size
        frame_size_data = client_socket.recv(16)
        # print(frame_size_data)
        if not frame_size_data:
            break

        frame_size = int(frame_size_data.strip())
        if frame_size == 0:
            break

        # Receive frame data
        frame_data = b''
        while len(frame_data) < frame_size:
            remaining_bytes = frame_size - len(frame_data)
            frame_data += client_socket.recv(remaining_bytes)

        # Convert frame data to numpy array
        frame_np = np.frombuffer(frame_data, dtype=np.uint8)

        # Decode frame
        frame = cv2.imdecode(frame_np, cv2.IMREAD_COLOR)
        # Resize frame to 720x1080
        frame = cv2.resize(frame, (1080, 720))
        
        # Display frame
        cv2.imshow('Video Stream', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

# Function to receive messages from the server
def receive_messages(client_socket):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            # Decrypt and display the received cipher text
            decrypted_message = decrypt_message(data)
            print(decrypted_message)

    except Exception as e:
        print(f"Error: {e}")
        client_socket.close()

# Function to decrypt a message using the client's private key
def decrypt_message(cipher_text):
    # Implement decryption logic using the client's private key
    return cipher_text.decode()

# Function to handle user input and send messages to the server
def send_messages(client_socket):
    try:
        while True:
            # Get recipient name and message from user input
            recipient_name = input("Enter recipient name: ")
            message = input("Enter message: ")

            # Encrypt message using recipient's public key
            if recipient_name in client_dict:
                recipient_public_key = RSA.import_key(client_dict[recipient_name])
                cipher_rsa = PKCS1_OAEP.new(recipient_public_key)
                encrypted_message = cipher_rsa.encrypt(message.encode())

                # Send encrypted message to the server
                client_socket.send(recipient_name+":"+encrypted_message)

    except KeyboardInterrupt:
        print("[*] Exiting.")
        client_socket.close()

# Function to handle video playback
def play_video(client_socket):
    # Request server to list available videos
    client_socket.send(b"List Available Videos")

    # Receive video list from server
    video_list = client_socket.recv(1024).decode()
    print("Available Videos:")
    print(video_list)

    # Request server to play a video
    video_name = input("Enter video file name to play: ")
    client_socket.send(f"Play {video_name}".encode())

# Create a client socket and connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

client_name = input("Enter your name: ")
# Generate RSA key pair
key = RSA.generate(2048)
public_key = key.publickey().export_key().decode()
client_socket.send(f"{client_name}:{public_key}".encode())

confirmation = client_socket.recv(1024).decode()
print(confirmation)

client_dict[client_name] = public_key


# Send client name and public key to the server
#client_name = input("Enter your name: ")
#public_key = input("Enter your public key: ")
#client_dict[client_name] = public_key

# Start a thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

# Start a thread to handle user input and send messages to the server
send_thread = threading.Thread(target=send_messages, args=(client_socket,))
send_thread.start()

# Start a thread to handle video playback
video_thread = threading.Thread(target=play_video, args=(client_socket,))
video_thread.start()

# Wait for threads to complete
receive_thread.join()
send_thread.join()
video_thread.join()
