import socket
import pickle
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Create a socket and connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000)
client_socket.connect(server_address)

# Generate RSA key pair
key = RSA.generate(2048)
public_key = key.publickey().export_key()

# Send client name and public key to the server
client_name = "client_1"  # Change this according to client name
client_data = {'name': client_name, 'public_key': public_key}
client_socket.send(pickle.dumps(client_data))

# Receive dictionary from the server
server_data = pickle.loads(client_socket.recv(1024))
client_dictionary = server_data['clients']

# Secure Communication
def encrypt_message(message, recipient_public_key):
    cipher = PKCS1_OAEP.new(RSA.import_key(recipient_public_key))
    return cipher.encrypt(message.encode())

def update_dictionary(data):
    global client_dictionary
    client_dictionary = data['clients']

# Function to handle receiving updated dictionary from server
def receive_updated_dictionary():
    global client_dictionary
    server_data = pickle.loads(client_socket.recv(1024))
    update_dictionary(server_data)

# Function to send encrypted message to the server
def send_encrypted_message(recipient_name, message):
    recipient_public_key = client_dictionary[recipient_name]['public_key']
    encrypted_message = encrypt_message(message, recipient_public_key)
    client_socket.send(pickle.dumps({'recipient': recipient_name, 'message': encrypted_message}))

# Example usage:
# Send encrypted message to client_2
send_encrypted_message("client_2", "This is a secret message")

# Receive updated dictionary from server
receive_updated_dictionary()

# Close the socket
client_socket.close()
