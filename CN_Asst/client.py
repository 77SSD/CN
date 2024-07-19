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
client_dict = {}

# Function to receive messages from the server
def receive_messages(client_socket, private_key):
    try:
        while True:
            data = client_socket.recv(4096)  # Increased buffer size to accommodate larger ciphertexts
            if not data:
                break

            # Decrypt and display the received cipher text
            decrypted_message = decrypt_message(data, private_key)
            print("Received message:", decrypted_message)

    except Exception as e:
        print(f"Error receiving message: {e}")
        client_socket.close()

# Function to decrypt a message using the client's private key
def decrypt_message(cipher_text, private_key):
    try:
        rsa_key = RSA.import_key(private_key)
        cipher_rsa = PKCS1_OAEP.new(rsa_key)
        decrypted_message = cipher_rsa.decrypt(cipher_text)
        return decrypted_message.decode('utf-8')
    except Exception as e:
        print(f"Error decrypting message: {e}")
        return None

# Function to receive the client dictionary from the server
def receive_client_dict(client_socket):
    # global client_dict
    try:
        while True:
            serialized_client_dict = client_socket.recv(4096)
            if not serialized_client_dict:
                break
            client_dict = pickle.loads(serialized_client_dict)
            print("Received client dictionary:", client_dict)  # Debug print
    except Exception as e:
        print(f"Error receiving client dictionary: {e}")

# Function to handle user input and send messages to the server
def send_messages(client_socket, public_key):
    try:
        while True:
            # # Get recipient name and message from user input
            # recipient_name = input("Enter recipient name: ")
            # message = input("Enter message: ")
            print("dict: ",client_dict)
            # Check if recipient is in the client dictionary
            if recipient_name in client_dict:
                print("rnsme: ", recipient_name)
                recipient_public_key = RSA.import_key(client_dict[recipient_name])
                cipher_rsa = PKCS1_OAEP.new(recipient_public_key)

                # Encrypt message using recipient's public key
                encrypted_message = cipher_rsa.encrypt(message.encode())

                # Send encrypted message to the server
                client_socket.send(encrypted_message)
            else:
                print("Recipient not found in client dictionary.")

    except KeyboardInterrupt:
        print("[*] Exiting.")
        client_socket.close()
    except Exception as e:
        print(f"Error sending message: {e}")
        client_socket.close()

# Create a client socket and connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

# Generate RSA key pair
key = RSA.generate(2048)

# Extract the public key
public_key = key.publickey().export_key()

# Encode the public key as Base64 and bytes
encoded_public_key = base64.b64encode(public_key)
public_key_bytes = encoded_public_key

# Send client name and public key to the server
client_name = input("Enter your name: ")
client_socket.send(client_name.encode())
client_socket.send(public_key_bytes)

# Start a thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages, args=(client_socket, key.export_key()))
receive_thread.start()

# Start a thread to receive the client dictionary from the server
client_dict_thread = threading.Thread(target=receive_client_dict, args=(client_socket,))
client_dict_thread.start()

# Start a thread to handle user input and send messages to the server
send_thread = threading.Thread(target=send_messages, args=(client_socket, public_key_bytes))
send_thread.start()

# Wait for threads to finish
send_thread.join()
receive_thread.join()
client_dict_thread.join()
