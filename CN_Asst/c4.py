import socket
import pickle
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

# Function to generate RSA key pair
def generate_rsa_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
server_address = ('0.0.0.0', 1500)

# Connect to the server
client_socket.connect(server_address)

# Generate RSA key pair
private_key, public_key = generate_rsa_key_pair()

# Serialize the public key
serialized_public_key = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Get client name from the user
client_name = input("Enter your name: ")

# Print client name and public key
print("Client name:", client_name)
print("Public key:", serialized_public_key.decode())

# Send client name and public key to the server
client_socket.send(client_name.encode())
client_socket.send(serialized_public_key)


# Receive dictionary of client details from the server
serialized_clients = client_socket.recv(4096)
clients = pickle.loads(serialized_clients)
#print(serialized_clients)
# Print the received dictionary of client details
print("\nDictionary of client details received from the server:")
print(clients)

# Close the connection
client_socket.close()
